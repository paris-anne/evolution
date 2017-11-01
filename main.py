import agent as ag
import numpy as np
import environment as env

envirox = 500.0
enviroy = 500.0
enviro = env.Environment(envirox, enviroy)
foodnumber = 49
enviro = env.Environment(envirox, enviroy)
enviro.add_agents(60)


for i in np.arange(2,envirox, envirox/np.sqrt(foodnumber)):
	for j in np.arange(2, enviroy, enviroy/np.sqrt(foodnumber)):
		print (i,j)
		enviro.addfood(i,j, 10)


# enviro.addfood(50.0, 50.0, 5)
# enviro.addfood(200.0, 200.0, 5)
# enviro.addfood(100.0, 50, 5)
# enviro.addfood(50.0, 50.0, 5)
# enviro.addfood(125.0, 125.0, 5)


enviro.display(100000)
enviro.plot()
Data = []

def get_pygame_events():
	pygame_events  = pygame.event.get()
	return pygame_events
# adjust levels to have good simulation
# add time factor 
