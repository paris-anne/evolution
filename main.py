import agent as ag
import environment as env

enviro = env.Environment(100, 100)
enviro.add_agents(10, speed = 3)
enviro.addfood(50, 50, 5)
enviro.display()
