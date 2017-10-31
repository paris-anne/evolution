import agent as ag
import numpy as np
import environment as env


envirox = 250.0
enviroy = 250.0
foodnumber = 10
enviro = env.Environment(envirox, enviroy)
enviro.add_agents(50)

for i in np.arange(1,foodnumber,1):
	enviro.addfood(envirox *i/foodnumber, enviroy * i/foodnumber, 5)


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
