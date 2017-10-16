import numpy as np

class Agent:

	def __init__(self, position, reproduce, environment):
		self.key = key
		self.__position = position
		self.__food_level = food_level
		self.__reproduce = reproduce
		self.__enviro = environment
	
	def position(self):
		return self.position

	def set_position(self, position):
		self.position = position
		return

	def food_level(self):
		return self.food_level

	def set_food_level(self, food_level):
		self.food_level = food_level
		return

	def reproduce(self):
		return self.reproduce

	def set_reproduce(self, reproduce):
		self.reproduce = reproduce
		return

	def enviro(self):
		return self.enviro

	def set_enviro(self, environment):
		self.enviro = environment
		return

	def reproduce(self):
		self.food_level = self.food_level / 2.0
		return Agent(self.position(), 0.5, self.reproduce(), self.enviro())

	def eat(self):
		self.food_level += 0.1
		return

	def die(self):
		self.enviro().remove_ag(key)

	def move(self):
		max_pos = enviro.max()
		min_pos = enviro.min()
		position = self.position()
		for i in position:
			if min_pos < i and i < max_pos:
				direction = np.random.randint(-1,1)
			elif position == max_pos:
				direction = np.random.randint(-1,0)
			else:
				direction = np.random.randint(0,1)
			i += direction
		self.set_position(position)
		self.food_level -= 0.1
		return

	def living_cycle(self):
		agent.move()
		if enviro.food(agent.pos()) == 1:
			agent.eat()
		if agent.food_level() == 1:
			agent.reproduce()
		elif agent.food_level() == 0:
			agent.die() 
		return
