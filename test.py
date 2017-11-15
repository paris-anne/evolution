import pandas as pd 
import environment as env
import agent as ag

enviro = env.Environment()
agents = []
for i in range(6):
	agent = ag.Agent(0, i, enviro)
	agents.append(agent)

data = pd.DataFrame.from_items([('agents', agents)])
def get_key(agent):
	return agent.key
data['agent_key'] = data['agents'].apply(get_key)
print(data)
