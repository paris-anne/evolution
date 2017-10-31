import agent as ag
import environment as env
# this is a new comment

envirox = 250.0
enviroy = 250.0
foodnumber = 10
enviro = env.Environment(envirox, enviroy)
enviro.add_agents(50)

for i in np.arange(1,foodnumber,1):
	foodx = np
	enviro.addfood(envirox *i/foodnumber, enviroy * i/foodnumber, 5)

enviro = env.Environment(0.1)

agent = Agent([0,0], 0.5, 1.0, enviro)
enviro.add_agent(agent.pos())

for i in range(100):
	agent.living_cycle()

