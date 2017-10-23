import agent as ag
import environment as env

enviro = env.Environment(100, 100)
enviro.add_particles()
enviro.display()

agent = ag.Agent([0,0], 0.5, 1.0, enviro)
enviro.add_agent(agent.pos())

for i in range(100):
	agent.living_cycle()

window = Window()
window.add_particles()
