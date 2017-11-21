import agent as ag
import numpy as np
import environment as env
import matplotlib.pyplot as pl
import datetime
import numpy as np
import random
import particle as p
import plots
import pandas as pd

envirox = 500
enviroy = 500
foodnumber = 10
enviro = env.Environment(envirox, enviroy)
enviro.addfood(0.2) #parameter is food_coverage as a proportion
enviro.add_antibiotics(0.5, 13000, 1000) #concentration, time between dose, halflife of dose
enviro.add_agents(100)
data = enviro.display(10000000)
data.to_string()
#df = data.iloc[:,-1].apply(lambda x: x.reproduce_level if (np.all(pd.notnull(x))) else x)
#df.to_csv('data.csv')
plots.plot(data)
