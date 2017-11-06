import agent as ag
import numpy as np
import environment as env
import matplotlib.pyplot as pl
import datetime
import numpy as np
import random
import plots

envirox = 100.0
enviroy = 100.0
foodnumber = 36
enviro = env.Environment(envirox, enviroy)
enviro.add_agents(20)
enviro.addfood(36)
data = enviro.display(100000)
print(data.to_string())
pl.plot(data['Time Elapsed'], data['Resistance'])
pl.show()

def get_pygame_events():
	pygame_events  = pygame.event.get()
	return pygame_events
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



