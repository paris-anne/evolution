import agent as ag
import numpy as np
import environment as env
import matplotlib.pyplot as pl
import datetime
import numpy as np
import random

envirox = 100.0
enviroy = 100.0
foodnumber = 36
enviro = env.Environment(envirox, enviroy)
enviro.add_agents(49)

# for i in np.arange(1,foodnumber,1):
# 		enviro.addfood(envirox *i/foodnumber, enviroy*i/foodnumber, 5)

for i in np.arange(0,envirox, envirox/np.sqrt(foodnumber)):
	for j in np.arange(0, enviroy, enviroy/np.sqrt(foodnumber)):
		print (i,j)
		enviro.addfood(i, j, 5)

# enviro.addfood(50.0, 50.0, 5)
# enviro.addfood(200.0, 200.0, 5)
# enviro.addfood(100.0, 50, 5)
# enviro.addfood(50.0, 50.0, 5)
# enviro.addfood(125.0, 125.0, 5)

enviro.display(100000)
enviro.population_plot()
enviro.dead_plot()
data = []

def get_pygame_events():
	pygame_events  = pygame.event.get()
	return pygame_events

# adjust levels to have good simulation
# add time factor 
