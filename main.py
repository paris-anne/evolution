import agent as ag
import environment as env

enviro = env.Environment(1000.0, 1000.0)
enviro.add_agents(100)
enviro.addfood(250.0, 250.0, 10)
enviro.addfood(750.0, 750.0, 10)
enviro.addfood(250.0, 750.0, 10)
enviro.addfood(750.0, 250.0, 10)

enviro.display()

# adjust levels to have good simulation
# add time factor 