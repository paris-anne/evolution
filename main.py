import agent as ag
import environment as env
import matplotlib.pyplot as pl
import datetime
import random

enviro = env.Environment(100.0, 100.0)
enviro.add_agents(100)
enviro.addfood(25.0, 25.0, 5)
enviro.addfood(75.0, 75.0, 5)
enviro.addfood(25.0, 75.0, 5)
enviro.addfood(75.0, 25.0, 5)
print(len(enviro.agents))
enviro.display()
population = enviro.get_population_time()
x = [datetime.datetime.now() + datetime.timedelta(hours=i) for i in range(len(population))]
pl.plot(x, population)
pl.show()
# adjust levels to have good simulation
# add time facto