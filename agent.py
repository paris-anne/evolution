import numpy as np
import environment as enviro
import particle as p
import random

class Agent(p.Particle):
	count = 0

	def __init__(self, x, y, environment, size = 3.0, colour = (0, 0, 255), speed = 1.0, reproduce_level = 10,  food_level = 5):
		super().__init__(x, y, size, colour, speed)
		self.key = self.count # need way of incrementing key
		self.food_level = food_level
		self.reproduce_level = reproduce_level
		self.size = size
		self.enviro = environment
		self.x = random.randint(self.size, self.enviro.width - self.size)
		self.y = random.randint(self.size, self.enviro.height - self.size)
		self.count +=1

	def reproduce(self):
		self.food_level = 5
		child = Agent(self.x, self.y, self.enviro)
		self.enviro.add_agent(child)

	def eat(self):
		foodpos_x = self.enviro.food.x
		foodpos_y = self.enviro.food.y
		#change food shape to square
		if np.sqrt((self.x - foodpos_x)**2 + (self.y - foodpos_y)**2) < self.enviro.food.size:
			self.food_level += 1

	def die(self):
		self.colour = (0, 255, 0)
