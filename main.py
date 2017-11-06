import agent as ag
import numpy as np
import environment as env
import matplotlib.pyplot as pl
import datetime
import numpy as np
import random
import plots
import particle as p

envirox = 200.0
enviroy = 200.0
foodnumber = 36
enviro = env.Environment(envirox, enviroy)
enviro.addfood()
enviro.add_agents(20)
#enviro.addfood(foodnumber)
data = enviro.display(100000)
#print(data.to_string())
pl.plot(data['Time Elapsed'], data['Resistance'])
plots.plot(data)


#enviro.display(500000)
# data = []

def get_pygame_events():
	pygame_events  = pygame.event.get()
	return pygame_events
