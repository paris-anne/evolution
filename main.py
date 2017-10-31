import agent as ag
import numpy as np
import environment as env

enviro = env.Environment(100.0, 100.0)
enviro.add_agents(100)
enviro.addfood(25.0, 25.0, 5)
enviro.addfood(25.0, 75.0, 5)
enviro.addfood(75.0, 75.0, 5)
enviro.addfood(75.0, 25.0, 5)
enviro.display(1000)

enviro.plot()
Data = []

def get_pygame_events():
	pygame_events  = pygame.event.get()
	return pygame_events
# adjust levels to have good simulation
# add time factor 
