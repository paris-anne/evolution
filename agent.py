import numpy as np

class Agent(Particle):

	def __init__(self, reproduce, environment):
		self.key = key
		self.food_level = food_level
		self.reproduce = reproduce
		self.enviro = environment

	def reproduce(self):
		self.food_level = self.food_level / 2.0
		child = Agent(self.reproduce, self.enviro)
		self.enviro.agents.append(child)
		self.enviro.add_particle(self.x, self.y, self.size, self.speed)

	def eat(self):
		self.food_level += 0.1
		return

	def die(self):
		self.enviro().remove_ag(key)

	def living_cycle(self):
		agent.move()
		if agent.pos()) == 1:
			agent.eat()
		if agent.food_level() == 1:
			agent.reproduce()
		elif agent.food_level() == 0:
			agent.die() 
		return
