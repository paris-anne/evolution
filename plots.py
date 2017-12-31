import matplotlib.pyplot as pl
import pandas as pd 
from scipy.optimize import curve_fit
import numpy as np
from scipy.integrate import odeint
import environment as enviro
import matplotlib.animation as animation
import environment as env

def run(first_dose, anti_conc, anti_freq, anti_halflife, skipped_doses,double_doses, numberofdoses, numberofagents, plotlabel=None): #first dose, anti_conc, yyf y 
	envirox = 600
	enviroy = 600
	enviro = env.Environment(envirox, enviroy)
	enviro.addfood(0.25)
	enviro.set_first_dose(first_dose)
	enviro.set_anti_conc(anti_conc)
	enviro.set_anti_freq(anti_freq)
	enviro.set_anti_halflife(anti_halflife) 
	enviro.set_skipped_doses(skipped_doses) 
	enviro.set_double_doses(double_doses)
	enviro.set_numberofdoses(numberofdoses)
	enviro.add_agents(numberofagents)
	enviro.set_plotlabel(plotlabel)
	data = enviro.display(250000, display = True)
	return data

def deaths(dataframes):
    time_elapsed = list(dataframes.columns.values)
    print(time_elapsed)
    print(dataframes)
    deathsbyimmune = dataframes.iloc[:,0].tolist()[0].enviro.deathsbyimmune
    deathsbyanti = dataframes.iloc[:,0].tolist()[0].enviro.deathsbyanti
    deathsbyfood = dataframes.iloc[:,0].tolist()[0].enviro.deathsbyfood
    pl.figure("Deathsplot") # + str(self.plotlabel)
    pl.plot(time_elapsed, deathsbyimmune, 'r', label = "immune system")
    pl.plot(time_elapsed, deathsbyanti, 'g', label = "antibiotics")
    pl.plot(time_elapsed, deathsbyfood, 'b', label = "movement")
    pl.title("Cause of Death")
    pl.xlabel("Time Elapsed")
    pl.ylabel("Frequency")
    pl.legend()
    pl.grid(True, which='both')
    pl.show()

def dormancy_count(dataframes):
    time_elapsed = list(dataframes.columns.values)
    dormant = dataframes.iloc[:,0].tolist()[0].enviro.dormancy_count
    pl.figure("Dormancy") # + str(self.plotlabel)
    pl.plot(time_elapsed, dormant)
    pl.title("Dormant Agents")
    pl.xlabel("Time Elapsed")
    pl.ylabel("Number of Agents Dormant")
    pl.legend()
    pl.grid(True, which='both')
    pl.show()

def dormancytime_hist(dataframes):
    time_elapsed = list(dataframes.columns.values)[-1]
    hist_data = dataframes.iloc[:,0].tolist()[0].enviro.hist_dormancy_time
    hist_freq = dataframes.iloc[:,0].tolist()[0].enviro.hist_freq
    frames = np.divide(time_elapsed, hist_freq)
    def update_hist(num, data):
        pl.cla()
        pl.hist(hist_data[num][0], ec = 'black')
        pl.title("Dormancy time distribution at time: " + str(hist_data[num][1] ))
        pl.xlabel("Dormancy time")
        pl.ylabel("Frequency")
    frames1 = int(frames - frames%1)
    fig = pl.figure(1001)
    ani = animation.FuncAnimation(fig, update_hist, frames1, fargs = (hist_data,))
    # ani.save('blaisematuidi.gif', writer = "imagemagick", fps=60)
    # print(animation.writers.list())
    pl.show()

def hist_2d_dormancy_time_vs_dormancy_freq(dataframes):
    time_elapsed = list(dataframes.columns.values)[-1]
    dormancy_time = dataframes.iloc[:,0].tolist()[0].enviro.hist_dormancy_time
    dormancy_freq = dataframes.iloc[:,0].tolist()[0].enviro.hist_dormancy_freq
    hist_freq = dataframes.iloc[:,0].tolist()[0].enviro.hist_freq

    frames = np.divide(time_elapsed, hist_freq)



    def update_hist(num, data):
        pl.clf()
        pl.hist2d(dormancy_time[num][0],dormancy_freq[num][0],bins =25)
        pl.title("Dormancy freq distribution at time: " + str(dormancy_time[num][1] ))
        pl.xlabel("Dormancy time")
        pl.ylabel("Dormancy freq")
        cb = pl.colorbar()
        cb.set_label('counts in bin')

    frames1 = int(frames - frames%1)

 
    # Writer = animation.writers['imagemagick']
    # writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    #writer = animation.ImageMagickFileWriter()
 
 
    fig = pl.figure(12)
    ani = animation.FuncAnimation(fig, update_hist, frames1, fargs = ((dormancy_time,dormancy_freq),))
    #ani.save('animation.gif', writer = "imagemagick")
    pl.show()

def finish_early(first_dose = 0, anti_conc = 0.01, anti_freq = 16000, anti_halflife = 4000, skipped_doses = [] , double_doses = [], numberofagents = 500):
    pl.figure("Finish Course Early") # + str(self.plotlabel)
    for i in range(1, 10):
        #print("dose {}".format(i))
        data = run(first_dose = first_dose, anti_conc = anti_conc, anti_freq = anti_freq, anti_halflife =anti_halflife, skipped_doses =skipped_doses, double_doses =double_doses, numberofagents =numberofagents, numberofdoses = i)
        pl.plot(list(data.columns.values), data.count(), label = "Stopped after {} doses".format(i))
    pl.title("Population vs time")
    pl.xlabel("Time Elapsed")
    pl.ylabel("Population")
    pl.grid(True, which='both')
    pl.legend()
    pl.show()

def dormancy_2d_hist(data, frames):
    offspring = pd.DataFrame(data.iloc[:,-1].dropna().apply(lambda x: x.reproduction))

    def update_hist(num, data):
        pl.clf()
        pl.hist2d(data[num][0], offspring, bins=50, cmap='Blues')
        pl.title("Dormancy time and offspring number distribution at: " + str(data[num][1]))
        pl.xlabel("Dormancy time")
        pl.ylabel("Number of offspring")
        cb = pl.colorbar()
        cb.set_label('counts in bin')

    frames1 = int(frames - frames%1)
    fig = pl.figure(11)
    ani = animation.FuncAnimation(fig, update_hist, frames1, fargs = (data, offspring))
    #ani.save('animation.gif', writer = "imagemagick")
    pl.show()

def skip_doses(skip, first_dose = 0, anti_conc = 0.01, anti_freq = 16000, anti_halflife = 4000, double_doses = [], numberofdoses = 10, numberofagents = 500):
    pl.figure("Skip Doses") # + str(self.plotlabel)
    miss = []
    for i in skip:
        miss.append(i)
        data = run(first_dose = first_dose, anti_conc = anti_conc, anti_freq = anti_freq, anti_halflife = anti_halflife, skipped_doses = miss , double_doses = double_doses, numberofdoses = numberofdoses, numberofagents = numberofagents) #first dose, anti_conc,
        pl.plot(list(data.columns.values), data.count(), label = "Missed doses: {}".format(miss))
    pl.title("Population vs time")
    pl.xlabel("Time Elapsed")
    pl.ylabel("Population")
    pl.grid(True, which='both')
    pl.legend()
    pl.show()

def skip_one_dose(first_dose = 0, anti_conc = 0.01, anti_freq = 16000, anti_halflife = 4000, double_doses = [], numberofdoses = 10, numberofagents = 500):
    pl.figure("Skip Doses") # + str(self.plotlabel)
    for i in range(1,11):
        data = run(first_dose = first_dose, anti_conc = anti_conc, anti_freq = anti_freq, anti_halflife = anti_halflife, skipped_doses = [i] , double_doses = double_doses, numberofdoses = numberofdoses, numberofagents = numberofagents) #first dose, anti_conc,
        pl.plot(list(data.columns.values), data.count(), label = "Missed dose: {}".format(i))
    pl.title("Population vs time")
    pl.xlabel("Time Elapsed")
    pl.ylabel("Population")
    pl.grid(True, which='both')
    pl.legend()
    pl.show()

def skip_two_doses(first_dose = 0, anti_conc = 0.01, anti_freq = 16000, anti_halflife = 4000, double_doses = [], numberofdoses = 10, numberofagents = 500):
    pl.figure("Skip 2 Doses") # + str(self.plotlabel)
    for i in range(1,10):
        data = run(first_dose = first_dose, anti_conc = anti_conc, anti_freq = anti_freq, anti_halflife = anti_halflife, skipped_doses = [i,i+1] , double_doses = double_doses, numberofdoses = numberofdoses, numberofagents = numberofagents) #first dose, anti_conc,
        pl.plot(list(data.columns.values), data.count(), label = "Missed doses: {}".format(str((i,i+1))))
    pl.title("Population vs time")
    pl.xlabel("Time Elapsed")
    pl.ylabel("Population")
    pl.grid(True, which='both')
    pl.legend()
    pl.show()

def skip_three_doses(first_dose = 0, anti_conc = 0.01, anti_freq = 16000, anti_halflife = 4000, double_doses = [], numberofdoses = 10, numberofagents = 500):
    pl.figure("Skip 3 Doses") # + str(self.plotlabel)
    for i in range(1,9):
        data = run(first_dose = first_dose, anti_conc = anti_conc, anti_freq = anti_freq, anti_halflife = anti_halflife, skipped_doses = [i,i+1,i+1] , double_doses = double_doses, numberofdoses = numberofdoses, numberofagents = numberofagents) #first dose, anti_conc,
        pl.plot(list(data.columns.values), data.count(), label = "Missed doses: {}".format(str((i,i+1, i+2))))

    pl.title("Population vs time")
    pl.xlabel("Time Elapsed")
    pl.ylabel("Population")
    pl.grid(True, which='both')
    pl.legend()
    pl.show()


def calibration(first_dose = 500000, anti_conc = 0.01, anti_freq = 16000, anti_halflife = 4000, skipped_doses = [], double_doses = [], numberofdoses = 10, numberofagents = 200):
    pl.figure("Normal person") # + str(self.plotlabel)
    for i in range(5):
        data = run(first_dose = first_dose, anti_conc = anti_conc, anti_freq = anti_freq, anti_halflife = anti_halflife, skipped_doses = skipped_doses, double_doses = double_doses, numberofdoses = numberofdoses, numberofagents = numberofagents) #first dose, anti_conc,
        pl.plot(list(data.columns.values), data.count(), label = "Run: {}".format(i+1))
    pl.title("Population vs time")
    pl.xlabel("Time Elapsed")
    pl.ylabel("Population")
    pl.xlim([0,500000])
    pl.ylim([0,400])
    pl.grid(True, which='both')
    pl.legend()
    pl.show()

def population(data):
    pl.figure("Population vs time")
    pl.plot(list(data.columns.values), data.count())
    pl.xlabel("Time Elapsed")
    pl.ylabel("Population")
    pl.grid()
    pl.show()

def reproductiondeathrates(dataframes):
    time_elapsed = list(dataframes.columns.values)
    print(time_elapsed)
    print(dataframes)
    reproductionrate_moving_average = dataframes.iloc[:,0].tolist()[0].enviro.reproduct_MA
    deathrate_moving_average = dataframes.iloc[:,0].tolist()[0].enviro.deaths_MA

    pl.figure("Moving averages for reproduction and death rate") # + str(self.plotlabel)
    pl.plot(time_elapsed, reproductionrate_moving_average, 'r', label = "Reproductions")
    pl.plot(time_elapsed, deathrate_moving_average, 'g', label = "Deaths")
    pl.title("Moving averages for reproduction and death rate")
    pl.xlabel("Time Elapsed")
    pl.ylabel("Frequency per ms")
    pl.legend()
    pl.grid(True, which='both')
    pl.show()       

def dPbydt_vs_P(dataframes):
    time_elapsed = list(dataframes.columns.values)
    print(time_elapsed)
    print(dataframes)
    reproductionrate_moving_average = dataframes.iloc[:,0].tolist()[0].enviro.reproduct_MA
    deathrate_moving_average = dataframes.iloc[:,0].tolist()[0].enviro.deaths_MA
    combined = np.subtract(reproductionrate_moving_average, deathrate_moving_average)
    population = dataframes.iloc[:,0].tolist()[0].enviro.population_count

    pl.figure("Rate of change of population as a function of population") # + str(self.plotlabel)
    # pl.scatter(population, combined)
    pl.scatter(population, reproductionrate_moving_average)
    slope, intercept = np.polyfit(population, reproductionrate_moving_average, 1)
    print(slope,intercept)

    pl.title("Rate of change of population as a function of population")
    pl.xlabel("Population")
    pl.ylabel("Rate of change of population")
    pl.legend()
    pl.grid(True, which='both')
    pl.show()    

def av_resistance(dataframes):
    av_resistance = dataframes.iloc[:,0].tolist()[0].enviro.av_resistance
    time_elapsed = list(dataframes.columns.values)
    pl.figure("averageresistacce")
    pl.plot(time_elapsed, av_resistance)
    pl.title("Average Resistance of Total Population")
    pl.xlabel("Time Elapsed")
    pl.ylabel("Average Resistance")
    pl.grid(True, which='major')
    pl.grid(True, which='minor')
    pl.show()

def resistant_total_pop(dataframes):
    time_elapsed = list(dataframes.columns.values)
    resistance = pd.DataFrame(dataframes.applymap(lambda x: x.resistance if (np.all(pd.notnull(x))) else x))
    resistant = resistance.apply(pd.value_counts).iloc[0,:].tolist()
    not_resistant = resistance.apply(pd.value_counts).iloc[1,:].tolist()
    pl.plot(time_elapsed, resistant, 'r', label = "Resistant")
    pl.plot(time_elapsed, not_resistant, 'g', label = "Not Resistant")
    pl.title("Population v Time")
    pl.xlabel("Time")
    pl.ylabel("Population")
    pl.legend()
    pl.grid(True, which='both')
    pl.show()
    resist_prop=np.divide(resistant, dataframes.count())
    pl.plot(time_elapsed, resist_prop)
    pl.title("Resistant Fraction of Total Population")
    pl.xlabel("Time")
    pl.ylim(0,1)
    pl.ylabel("Fraction Resistant")
    pl.grid(True, which='major')
    pl.grid(True, which='minor')
    pl.show()

#I HAVENT DONE THE PLOTS BELOW
def plot(dataframe):
    ax1 = pl.subplot(511)
    pl.plot(dataframe.loc(0), dataframe['Population'])
    ax1.title.set_text("Population") # add caption
    pl.plot(dataframe['Time Elapsed'], dataframe["Population"])
    pl.setp(ax1.get_xticklabels(), fontsize=6)
    ax2 = pl.subplot(412, sharex=ax1) 
    ax2.title.set_text("Death Rate")
    pl.plot(dataframe['Time Elapsed'], dataframe['Deadcount'])      
    pl.setp(ax2.get_xticklabels(), visible=False)
    ax3 = pl.subplot(413, sharex=ax1)
    ax3.title.set_text("Reproduction Rate")
    pl.plot(dataframe['Time Elapsed'], dataframe['Reproduction'])
    # ax4 = pl.subplot(514, sharex=ax1)
    # pl.plot(dataframe['Time Elapsed'], dataframe['Resistance'])
    # pl.setp(ax3.get_xticklabels(), visible=False)
    # ax4.title.set_text("Resistance")
    # ax5 = pl.subplot(515, sharex=ax1)
    # pl.plot(dataframe['Time Elapsed'], dataframe['Reproduction Count'])
    # pl.setp(ax4.get_xticklabels(), visible=False)
    # ax5.title.set_text("Reproduction Count")
    ax4 = pl.subplot(414)
    ax4.title.set_text("Food Population")
    pl.plot(dataframe['Time Elapsed'], dataframe['Food Population'])
    pl.savefig('plots.png')
    pl.show()
 
def func(x, a, c, d):
    return a*np.exp(c*x)+d
 
def LotkaVolterra(state,t):
  #x = state[0]
  y = state[0]
  alpha = 0.
  beta =  0.
  sigma = .001154
  gamma = 0.00008365
  #xd = x*(alpha - beta*y)
  yd = -y*(gamma - sigma*0.1)
  return [yd]
 
def LV_plots(dataframe):
    dataframe = dataframe.ix[:,1:-1]
    # t['time'] = dataframe.columns
    t=dataframe.count()
    df = pd.DataFrame(t.dropna())
    df.reset_index(level=0, inplace=True)   
    df.iloc[:,0] = pd.to_numeric(df.iloc[:,0], errors='coerce')
    t = df.iloc[:,0].values
    pop = df.iloc[:,1].values
    # state0 = [20]
    # state = odeint(LotkaVolterra, state0, t)
    # popt, pcov = curve_fit(func, list(dataframe), population.ix[0].tolist(), p0=(1, 1e-6, 1))
    # print(popt)
    # food=[0.1] * len(df.ix[:,0].values)
    ax1 = pl.subplot(211)
    ax1.title.set_text("Bacteria Population")
    print(df.ix[:,0].values)
    pl.plot(t, pop)
    #pl.plot(t, state)
    #pl.plot(list(dataframe), func(np.array(list(dataframe)), -1.71109885e-06, 4.26620601e-08, 2.00000017e+01))
    # pl.setp(ax1.get_xticklabels(), visible=False)
    # ax2 = pl.subplot(212, sharex=ax1)
    # ax2.title.set_text("Food Concentration")
    # pl.plot(df.ix[:,0].values, food)
    # pl.setp(ax2.get_xticklabels(), fontsize=6)
    pl.savefig("LV_equations.png")
    pl.show()
 
def plot_population(data):
    dataframe = dataframe.ix[:,1:-1]
    df = pd.DataFrame(t.dropna())
 
def offspring_analysis(data):
    offspring = data.iloc[:, -1].apply(lambda x: x.reproduction if (np.all(pd.notnull(x))) else x)
    foodlevel = data.iloc[:, -1].apply(lambda x: x.food_level if (np.all(pd.notnull(x))) else x)
    merge = pd.concat([offspring, foodlevel], axis=1)
    merge.to_csv("offspring_v_foodlevel.csv")
 
def antibiotic_conc_v_population(data):
    population=pd.DataFrame(data.count())
    #print(da)
    antibiotics=data.iloc[0,:].apply(lambda x: x.enviro.antibiotics_effectiveness)
    #print(antibiotics)
    ax1 = pl.subplot(211)
    ax1.title.set_text("Bacteria Population")
    pl.plot(list(data), population.ix[:,0])
    pl.setp(ax1.get_xticklabels(), visible=False)
    ax2 = pl.subplot(212, sharex=ax1)
    ax2.title.set_text("Antibiotics Concentration")
    pl.plot(list(data), antibiotics)
    pl.setp(ax2.get_xticklabels(), fontsize=6)
    pl.savefig("antibiotics_bacteria.png")
    #pl.show()   
 
def histogram(data):
    df = pd.DataFrame(data.iloc[:,-1])
    df = df.dropna()
    offspring = pd.DataFrame(data.iloc[:,-1].dropna().apply(lambda x: x.reproduction))
    dormancy = pd.DataFrame(data.iloc[:,-1].dropna().apply(lambda x: x.dormancy_time))
    print(offspring.iloc[:,0].values)
    pl.hist2d(offspring.iloc[:,0].values, dormancy.iloc[:,0].values, bins=100, cmap='Blues')
    cb = pl.colorbar()
    cb.set_label('counts in bin')
    pl.savefig("histogram.png")
    #pl.show()
 
def resistance(data):
    #resistance = pd.DataFrame.sum(data.iloc[:,-1].dropna().apply(lambda x: x.resistance))
    #print(resistance, "resistance")
    print(data.iloc['resistance':,-1].dropna())
 

def histogram(data):
    df = pd.DataFrame(data.iloc[:,-1])
    df = df.dropna()
    offspring = pd.DataFrame(data.iloc[:,-1].dropna().apply(lambda x: x.reproduction))
    dormancy = pd.DataFrame(data.iloc[:,-1].dropna().apply(lambda x: x.dormancy_time))
    print(offspring.iloc[:,0].values)
    pl.hist2d(offspring.iloc[:,0].values, dormancy.iloc[:,0].values, bins=100, cmap='Blues')
    cb = pl.colorbar()
    cb.set_label('counts in bin')
    pl.savefig("histogram.png")
    #pl.show()
 
def generations_hist(data, frames):
    #offspring = pd.DataFrame(data.iloc[:,-1].dropna().apply(lambda x: x.reproduction))
    time = data[0]
    freq = data[1]

    def update_hist(num, data):
        pl.clf()
        pl.hist2d(time[num], freq[num], bins=50, cmap='Blues')
        pl.title("Dormancy time and offspring number distribution at: " + str(data[num][1]))
        pl.xlabel("Dormancy time")
        pl.ylabel("Number of offspring")
        cb = pl.colorbar()
        cb.set_label('counts in bin')
 
    frames1 = int(frames - frames%1)
 
    # Writer = animation.writers['imagemagick']
    # writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    #writer = animation.ImageMagickFileWriter()
 
 
    fig = pl.figure(11)
 
    ani = animation.FuncAnimation(fig, update_hist, frames1, fargs = (time,freq))
    #ani.save('animation.gif', writer = "imagemagick")
    pl.show()
 
 
# def dormancytime_hist(hist_data, frames):
#     def update_hist(num, data):
#         pl.cla()
#         pl.hist(hist_data[num][0])
#         pl.title("Dormancy time distribution at time: " + str(hist_data[num][1] ))
#         pl.xlabel("Dormancy time")
#         pl.ylabel("Frequency")
#     frames1 = int(frames - frames%1)
 
#     # Writer = animation.writers['imagemagick']
#     # writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
#     #writer = animation.ImageMagickFileWriter()
 
 
#     fig = pl.figure(1001)
#     # ani = animation.FuncAnimation(fig, update_hist, frames1, fargs = (hist_data,))
#     # ani.save('blaisematuidi.gif', writer = "imagemagick", fps=60)
#     # print(animation.writers.list())
 
#     pl.show()
 
# def dormancyfreq_hist(hist_data, frames):
#     def update_hist(num, data):
#         pl.cla()
#         pl.hist2d(hist_data[0][num][0],hist_data[1][num][0],bins =25)
#         pl.title("Dormancy freq distribution at time: " + str(hist_data[0][num][1] ))
#         pl.xlabel("Dormancy freq")
#         pl.ylabel("Frequency")
#     frames1 = int(frames - frames%1)
 
#     # Writer = animation.writers['imagemagick']
#     # writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
#     #writer = animation.ImageMagickFileWriter()
 
 
#     fig = pl.figure(12)
#     ani = animation.FuncAnimation(fig, update_hist, frames1, fargs = (hist_data,))
#     #ani.save('animation.gif', writer = "imagemagick")
#     pl.show()
 
def dormancyfreqplustime_hist(hist_data, frames):
    def update_hist(num, data):
        pl.cla()
        pl.hist(hist_data[num][0])
        pl.title("Dormancy freq + time distribution at time: " + str(hist_data[num][1] ))
        pl.xlabel("Dormancy freq + time")
        pl.ylabel("Frequency")
    frames1 = int(frames - frames%1)
 
    # Writer = animation.writers['imagemagick_file']
    # writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    #writer = animation.ImageMagickFileWriter()
     
    # FFMpegWriter = manimation.writers['ffmpeg']
    # metadata = dict(title='Movie Test', artist='Matplotlib',
 #                comment='Movie support!')
    # writer = FFMpegWriter(fps=15, metadata=metadata)
 
 
 
    fig = pl.figure(13)
    ani = animation.FuncAnimation(fig, update_hist, frames1, fargs = (hist_data,))
    #ani.save('animation.gif', writer = "imagemagick_file")
    #pl.show()



def deaths(dataframes):
    time_elapsed = list(dataframes.columns.values)
    print(time_elapsed)
    print(dataframes)
    deathsbyimmune = dataframes.iloc[:,0].tolist()[0].enviro.deathsbyimmune
    deathsbyanti = dataframes.iloc[:,0].tolist()[0].enviro.deathsbyanti
    deathsbyfood = dataframes.iloc[:,0].tolist()[0].enviro.deathsbyfood

    cum_deathsbyimmune = np.cumsum(deathsbyimmune)
    cum_deathsbyanti = np.cumsum(deathsbyanti)
    cum_deathsbyfood = np.cumsum(deathsbyfood)




    pl.figure("Deathsplot") # + str(self.plotlabel)
    pl.plot(time_elapsed, deathsbyimmune, 'r', label = "immune system")
    pl.plot(time_elapsed, deathsbyanti, 'g', label = "antibiotics")
    pl.plot(time_elapsed, deathsbyfood, 'b', label = "movement")
    pl.title("Cause of Death")
    pl.xlabel("Time Elapsed")
    pl.ylabel("Frequency")
    pl.legend()
    pl.grid(True, which='both')

    pl.figure("Cumulative Deathsplot") # + str(self.plotlabel)
    pl.plot(time_elapsed, cum_deathsbyimmune, 'r', label = "immune system")
    pl.plot(time_elapsed, cum_deathsbyanti, 'g', label = "antibiotics")
    pl.plot(time_elapsed, cum_deathsbyfood, 'b', label = "movement")
    pl.title("Cause of Death")
    pl.xlabel("Time Elapsed")
    pl.ylabel("Frequency")
    pl.legend()
    pl.grid(True, which='both')
    pl.show()

    # pl.figure(2)
    # pl.plot(self.time_elapsed, self.av_resistance, label='Miss dose number: ' + str(self.plotlabel))
    # pl.title("Average resistance")
    # pl.xlabel("Time Elapsed")
    # pl.ylabel("Average resistance")
    # pl.legend()
    # pl.grid(True, which='both')




    # pl.figure("pop/res plot, individual, missing dose no " +str(self.plotlabel) )
    # pl.plot(self.time_elapsed, pop, label='Total Population')
    # pl.plot(self.time_elapsed, self.resistancepop, label = "'Resistant Population'")
    # pl.title("Population vs time")
    # pl.xlabel("Time Elapsed")
    # pl.ylabel("Population")
    # pl.grid(True, which='both')
    # pl.legend()

    # pl.figure("deathsplotcum " + str(self.plotlabel))
    # pl.plot(self.time_elapsed, self.deathsbyimmune, label = "immune system")
    # pl.plot(self.time_elapsed, self.deathsbyanti, label = "antibiotics")
    # pl.plot(self.time_elapsed, self.deathsbyfood, label = "movement")
    # pl.title("Cumulative Cause of Death")
    # pl.xlabel("Time Elapsed")
    # pl.ylabel("Frequency")
    # pl.grid(True, which='both')
    # pl.legend()

    # pl.figure(100 )
    # pl.plot(self.time_elapsed, pop, label='Miss dose number: ' + str(self.plotlabel))
    # pl.title("Population vs time")
    # pl.xlabel("Time Elapsed")
    # pl.ylabel("Population")
    # pl.grid(True, which='both')
    # pl.legend()

    # pl.figure("number dormant")
    # pl.plot(self.time_elapsed, self.avnumberdormant, label = "dormant pop")
    # pl.title("dormant")

    # print(self.time_ms)
    # plots.dormancytime_hist(self.hist_dormancy_time, self.time_ms/self.hist_freq)

