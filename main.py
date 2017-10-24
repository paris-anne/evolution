import agent as ag
import environment as env

enviro = env.Environment(100.0, 100.0)
enviro.add_agents(55)
enviro.addfood(50.0, 50.0, 10)
enviro.display()