import agent as ag
import numpy as np
import environment as env
import matplotlib.pyplot as pl
import datetime
import numpy as np
import random
import particle as p

envirox = 100
enviroy = 100
foodnumber = 10
enviro = env.Environment(envirox, enviroy)
enviro.add_agents(1)
enviro.addfood()


enviro.display(500000)
enviro.plot()
# data = []

def get_pygame_events():
	pygame_events  = pygame.event.get()
	return pygame_events




