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
envirox = 300
enviroy = 300
foodnumber = 10
enviro = env.Environment(envirox, enviroy)
enviro.addfood(0.1) #parameter is food_coverage as a proportion

enviro.add_agents(250) #100?
enviro.add_antibiotics(0.1, 43200, 14400) #concentration, time between dose(s) , halflife of dose
# #enviro.add_antibiotics(0.2, 13000, 1000) #concentration, time between dose, halflife of dose
data = enviro.display(1200000) #24 hours = 86400
data.to_pickle("population.pkl")
#plots.histogram(data)
# #plots.LV_plots(data)
# # df=enviro.plot()
# plots.plot(df)
# print(data)
#plots.population(data)
#plots.antibiotic_conc_v_population(data)

#df = pd.read_csv('bacteria_wo_antibiotics.csv', low_memory=False)
#plots.LV_plots(df)
