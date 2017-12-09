import agent as ag
import numpy as np
import environment as env
import matplotlib.pyplot as pl
import datetime
import numpy as np
import random
import particle as p
import plots
import food as f 
import pandas as pd

# pre antibiotics & normal amount of bacteria - 50 agents, immune system 3000, 10%, 1200000 time
# working antibiotics: antibiotics(0.1, 43200, 14400); agents = 250
envirox = 500
enviroy = 500
enviro = env.Environment(envirox, enviroy)
enviro.addfood(0.25) #parameter is food_coverage as a proportion

#enviro.add_agents(50) #100?
#enviro.add_antibiotics(0.1, 43200/2, 14400/2) #concentration, time between dose(s) , halflife of dose
#enviro.add_antibiotics(0.2, 13000, 1000) #concentration, time between dose, halflife of dose
#data = enviro.display(200000, display = True) #24 hours = 86400
#pop=pd.DataFrame({"population" :data.count()})
#print(pop["population"].iloc[-1])
#ntibioticse=data.iloc[0,:]
#print(data)
#print (df, "sdds==================================")
#plotdormancy_period = np.random.uniform(10000,40000)s.histogram(data)
#plots.LV_plots(data)
#df=enviro.plot()
#plots.plot(data)
#print(data)
#plots.population(data)
#plots.resistance(data)
#plots.antibiotic_conc_v_population(data)

def run(first_dose, anti_conc, anti_freq, anti_halflife, skipped_doses,double_doses, numberofdoses, numberofagents): #first dose, anti_conc,
	enviro.set_first_dose(first_dose)
	enviro.set_anti_conc(anti_conc)
	enviro.set_anti_freq(anti_freq)
	enviro.set_anti_halflife(anti_halflife)	
	enviro.set_skipped_doses(skipped_doses)	
	enviro.set_double_doses(double_doses)
	enviro.set_numberofdoses(numberofdoses)
	enviro.add_agents(numberofagents)
	data = enviro.display(300000, display = True)
	data[0].to_pickle("resistant.pkl")
	data[1].to_pickle("total.pkl")
	print(list(data[2]['time'].values))
	print(list(data[2]['dormancy'].values))
	pl.plot(list(data[2]['time'].values), list(data[2]['dormancy'].values))
	pl.show()
	#plots.population(data)

def changing_conc():
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

def changing_freq():
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
		data = enviro.display(200000, display = True)
		pop=pd.DataFrame({"population" :data.count()})
		final_pop = int((pop["population"].iloc[-1]))

		conc.append(i)
		fin.append(final_pop)
		print(fin)
	#pl.plot(conc, fin)
	pl.show()

run(first_dose = 0, anti_conc = 0.02, anti_freq = 16000, anti_halflife = 4000, skipped_doses = [] , double_doses = [], numberofdoses = 10, numberofagents = 500) #first dose, anti_conc,
#changing_starttime()
#antibiotics(0.1, 43200, 14400); agents = 250
#df = pd.read_csv('bacteria_wo_antibiotics.csv', low_memory=False)
#plots.LV_plots(df)