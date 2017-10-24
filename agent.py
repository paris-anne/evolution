import numpy as np
import environment as enviro
import particle as p
import random

class Agent(p.Particle):
	count = 0

	def __init__(self, x, y, environment, size = 3.0, colour = (0, 0, 255), speed = 0.8, reproduce_level = 15,  food_level = 5):
		super().__init__(x, y, size, colour, speed)
		self.key = self.count # need way of incrementing key
		self.food_level = food_level
		self.reproduce_level = reproduce_level
		self.size = size
		self.enviro = environment
		self.x = x
		self.y = y
		self.count +=1

	def reproduce(self):
		self.food_level = 5
		child = Agent(self.x, self.y, self.enviro)
		self.enviro.add_agent(child)

	def eat(self):
		for food in self.enviro.food:
			foodpos_x = food.x
			foodpos_y = food.y
			if np.sqrt((self.x - foodpos_x)**2 + (self.y - foodpos_y)**2) < food.size:
				self.food_level += 1

	def die(self):
		self.colour = (255, 0, 0)
		self.speed = 0
