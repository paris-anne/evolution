import agent as ag
import numpy as np
import environment as env

envirox = 1000.0
enviroy = 1000.0
foodnumber = 25
enviro = env.Environment(envirox, enviroy)
enviro.add_agents(1)

# for i in np.arange(1,foodnumber,1):
# 		enviro.addfood(envirox *i/foodnumber, enviroy*i/foodnumber, 5)

for i in np.arange(0,envirox, envirox/np.sqrt(foodnumber)):
	for j in np.arange(0, enviroy, enviroy/np.sqrt(foodnumber)):
		print (i,j)
		enviro.addfood(i,j, 5)



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
