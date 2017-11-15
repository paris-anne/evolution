import numpy as np
import environment as enviro
import particle as p
import random

class Agent(p.Particle):
	key = -1
	random = np.random.choice([0, 1], 1, p = [0.9, 0.1])
	def __init__(self, x, y, environment, size = 3.0, colour = (0, 0, 255), reproduce_level = 4.5,  food_level = 1.0, resistance = random, reproduction = 2):
		super().__init__(x, y, size, colour)
		# need way of incrementing key
		self.food_level = food_level
		self.fitness_cost = 0.3
		self.size = size
		self.enviro = environment
		self.x = x
		self.y = y
		self.resistance = resistance
		self.reproduce_level = reproduce_level + (self.resistance * self.fitness_cost)
		self.reproduction = reproduction
		Agent.key += 1

	def reproduce(self):
		self.food_level = self.food_level/self.reproduction
		for i in range(self.reproduction):
			reproduction = [2, 4]
			child_resistance = np.random.choice([self.resistance[0], (1-self.resistance[0])], 1, p = [0.9, 0.1])
			reproduction.remove(self.reproduction)
			child_reproduction = np.random.choice([self.reproduction, reproduction[0]] , 1, p = [0.9, 0.1])
			child = Agent(self.x, self.y, self.enviro, resistance = child_resistance, reproduction = child_reproduction[0])
			self.enviro.add_agent(child)

	def eat(self):
		for food in self.enviro.food:
			foodpos_x = food.x
			foodpos_y = food.y
			#print(np.sqrt((self.x - foodpos_x)**2 + (self.y - foodpos_y)**2))

			if 0.95 * food.size < np.sqrt((self.x - foodpos_x)**2 + (self.y - foodpos_y)**2) < 1 * 1.05 *food.size:
				self.food_level += 1.0

	def neutralise(self,i):
		for antibiotic in self.enviro.antibiotics:
			antibiotics_x = antibiotic.x
			antibiotics_y = antibiotic.y
			# print(np.sqrt((self.x - antibiotics_x)**2 + (self.y - antibiotics_y)**2))
			# print("------------------------------------------------------------")
			if 0.9 * antibiotic.size < np.sqrt((self.x - antibiotics_x)**2 + (self.y - antibiotics_y)**2) < 1 * 1.1 *antibiotic.size:
				if i not in self.enviro.dead_key:
					self.enviro.dead_key.append(i)
					print("NEUTRALISE")


	def die(self):
		self.enviro.remove_agent(self.key)
