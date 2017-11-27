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

envirox = 300
enviroy = 300
foodnumber = 10
enviro = env.Environment(envirox, enviroy)
enviro.addfood(0.1) #parameter is food_coverage as a proportion
# # enviro.add_antibiotics(0.006, 10000)
# #enviro.add_antibiotic(250,250,50)
enviro.add_agents(100) #100?
#enviro.add_antibiotics(0.1, 25000, 1000) #concentration, time between dose, halflife of dose
# #enviro.add_antibiotics(0.2, 13000, 1000) #concentration, time between dose, halflife of dose
data = enviro.display(250000)
plots.histogram(data)
# #plots.LV_plots(data)
# # df=enviro.plot()
# plots.plot(df)
# print(data)
#plots.plot(data)
#plots.antibiotic_conc_v_population(data)

#df = pd.read_csv('bacteria_wo_antibiotics.csv', low_memory=False)
#plots.LV_plots(df)
