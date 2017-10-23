import agent as ag
import environment as env

enviro = env.Environment(100, 100)
enviro.add_particles()
enviro.run()
enviro.addfood()
enviro.display()

