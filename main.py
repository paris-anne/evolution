import agent as ag
import environment as env
# this is a new comment
enviro = env.Environment(0.1)

agent = Agent([0,0], 0.5, 1.0, enviro)
enviro.add_agent(agent.pos())

for i in range(100):
	agent.living_cycle()

