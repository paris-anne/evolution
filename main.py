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
enviro.addfood(0.2) #parameter is food_coverage as a proportion
#enviro.add_antibiotics(0.01) #concentration is a proportion of area for now, can change into mg/L later
enviro.add_agents(20)

data = enviro.display(100000)
#print(data.to_string())
pl.plot(data['Time Elapsed'], data['Resistance'])
plots.plot(data)

def food_relation():
	foodnumber = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121]
	x = []
	y = []
	for i in foodnumber:
		enviro = env.Environment(envirox, enviroy)
		enviro.add_agents(100)
		enviro.addfood(i)
		x.append((i*(np.pi * enviro.food[0].size*enviro.food[0].size))/(enviroy*envirox))
		population = enviro.display(5000)
		y.append(population[-1])

	pl.plot(x, y)
	pl.show()
