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
	population(data)
	return enviro

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
 
def population(data):
    population=pd.DataFrame(data[1].count())
    print(population)
    pl.plot(list(data[1]), population.ix[:,0])
    # pl.setp(ax1.get_xticklabels(), visible=False)
    # ax2 = pl.subplot(212, sharex=ax1)
    # ax2.title.set_text("Antibiotics Concentration")
    # pl.plot(list(data), antibiotics)
    # pl.setp(ax2.get_xticklabels(), fontsize=6)
    # pl.savefig("bacteria_population.png")
    pl.show()
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
 
    # Writer = animation.writers['imagemagick']
    # writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    #writer = animation.ImageMagickFileWriter()
 
 
    fig = pl.figure(11)
 
    ani = animation.FuncAnimation(fig, update_hist, frames1, fargs = (data, offspring))
    #ani.save('animation.gif', writer = "imagemagick")
    pl.show()
 
 
def dormancytime_hist(hist_data, frames):
    def update_hist(num, data):
        pl.cla()
        pl.hist(hist_data[num][0])
        pl.title("Dormancy time distribution at time: " + str(hist_data[num][1] ))
        pl.xlabel("Dormancy time")
        pl.ylabel("Frequency")
    frames1 = int(frames - frames%1)
 
    # Writer = animation.writers['imagemagick']
    # writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    #writer = animation.ImageMagickFileWriter()
 
 
    fig = pl.figure(1001)
    # ani = animation.FuncAnimation(fig, update_hist, frames1, fargs = (hist_data,))
    # ani.save('blaisematuidi.gif', writer = "imagemagick", fps=60)
    # print(animation.writers.list())
 
    pl.show()
 
def dormancyfreq_hist(hist_data, frames):
    def update_hist(num, data):
        pl.cla()
        pl.hist(hist_data[num][0])
        pl.title("Dormancy freq distribution at time: " + str(hist_data[num][1] ))
        pl.xlabel("Dormancy freq")
        pl.ylabel("Frequency")
    frames1 = int(frames - frames%1)
 
    # Writer = animation.writers['imagemagick']
    # writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    #writer = animation.ImageMagickFileWriter()
 
 
    fig = pl.figure(12)
    ani = animation.FuncAnimation(fig, update_hist, frames1, fargs = (hist_data,))
    #ani.save('animation.gif', writer = "imagemagick")
    #pl.show()
 
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

def plot(i):
        pl.figure(3)
        pl.plot(self.time_elapsed, pop)
        pl.title("Population vs time")
        pl.xlabel("Time Elapsed")
        pl.ylabel("Population")
        pl.grid(True, which='both')
 
def changing_conc(enviro):
    conc = []
    fin = []
    for i in np.arange(0.1,0.5,0.1):
        enviro.remove_agents_and_anti()
        enviro.set_first_dose(2000)
        enviro.set_anti_conc(i)
        enviro.set_anti_freq(10000)
        enviro.set_anti_halflife(10000) 
        enviro.set_skipped_doses([2,5]) 
        enviro.add_agents(50)
        data = enviro.display(300000, display = True)
        pop=pd.DataFrame({"population" :data.count()})
        final_pop = int((pop["population"].iloc[-1]))
        conc.append(i)
        fin.append(final_pop)
        print(fin)
    pl.plot(conc, fin)
    pl.show()
 
def changing_freq(enviro):
    freq = []
    fin = []
    for i in np.arange(10000,40000,10000):
        enviro.remove_agents_and_anti()
        enviro.set_first_dose(2000)
        enviro.set_anti_conc(0.3)
        enviro.set_anti_freq(i)
        enviro.set_anti_halflife(10000) 
        enviro.set_skipped_doses([2,5]) 
        enviro.add_agents(50)
        data = enviro.display(300000, display = True)
        pop=pd.DataFrame({"population" :data.count()})
        final_pop = int((pop["population"].iloc[-1]))
 
        conc.append(i)
        fin.append(final_pop)
        print(fin)
    pl.plot(conc, fin)
    pl.show()

def skip_doses():
	for i in range(1, 10):
		print("dose {}".format(i))
		main.run(first_dose = 0, anti_conc = 0.01, anti_freq = 16000, anti_halflife = 4000, skipped_doses = [i] , double_doses = [], numberofdoses = 10, numberofagents = 500, plotlabel = "Stop after " + str(i) + " treatments") #first dose, anti_conc,

def skip_double_doses():
	for i in range(1, 9):
		run(first_dose = 0, anti_conc = 0.01, anti_freq = 16000, anti_halflife = 4000, skipped_doses = [i, i+1] , double_doses = [], numberofdoses = 10, numberofagents = 500, plotlabel = str(i))
		pl.show()
