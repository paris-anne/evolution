import agent as ag
import window
import environment as env

# this is a new comment\
# more context added.
enviro = env.Environment(0.1)
enviro.create()
enviro.add_particles()
enviro.run()

agent = ag.Agent([0,0], 0.5, 1.0, enviro)
enviro.add_agent(agent.pos())

for i in range(100):
	agent.living_cycle()

window = Window()
window.add_particles()
