import agent as ag
import numpy as np
import environment as env
import matplotlib.pyplot as pl
import datetime
import numpy as np
import random
import particle as p
import plots

envirox = 500
enviroy = 500
foodnumber = 10
enviro = env.Environment(envirox, enviroy)
enviro.addfood(0.1) #parameter is food_coverage as a proportion
enviro.add_antibiotics(0.006, 10000) #concentration is a proportion of area for now, can change into mg/L later
#enviro.add_antibiotic(250,250,50)
enviro.add_agents(30)
data = enviro.display(10000000)
print(data)
#plots.plot(data)
data.to_csv("dataframe.csv")