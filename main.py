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
enviro.add_agents(20)
enviro.addfood(36)



# enviro.addfood(50.0, 50.0, 5)
# enviro.addfood(200.0, 200.0, 5)
# enviro.addfood(100.0, 50, 5)
# enviro.addfood(50.0, 50.0, 5)
# enviro.addfood(125.0, 125.0, 5)

enviro.display(100000)
enviro.plot()
data = []

def get_pygame_events():
	pygame_events  = pygame.event.get()
	return pygame_events

# adjust levels to have good simulation
# add time factor 
