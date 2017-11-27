import numpy as np
import environment as enviro
import particle as p
import random

class Agent(p.Particle):
	key = -1
	random = np.random.choice([0, 1], p = [0.9, 0.1])
	def __init__(self, x, y, environment, size = 3.0, colour = (0, 0, 255), reproduce_level = 3.5,  food_level = float(2.0), resistance = 2, reproduction = np.random.choice([2.0, 3.0, 4.0, 5.0, 6.0], p = [0.99, 0.0025, 0.0025, 0.0025, 0.0025]), dormancy_gene = 1, dormancy_time = 700):
		super().__init__(x, y, size, colour)
		self.food_level = food_level
		self.fitness_cost = 0.3
		self.size = size
		self.enviro = environment
		self.x = x
		self.y = y
		self.resistance = resistance
		self.reproduce_level = reproduce_level #+ (self.resistance * self.fitness_cost)
		self.reproduction = reproduction
		self.dormancy_gene = dormancy_gene
		self.dormancy_time = dormancy_time
		#self.dormancy_freq
		Agent.key += 1

	def reproduce(self):
		new_foodlevel = self.food_level/float(self.reproduction)
		self.food_level = new_foodlevel
		for i in range(int(self.reproduction)):
			reproduction = [2.0, 3.0, 4.0, 5.0, 6.0]
			child_resistance = np.random.choice([self.resistance, (1-self.resistance)], p = [0.9, 0.1])
			reproduction.remove(self.reproduction)
			reproduction.append(self.reproduction)
			child_reproduction = np.random.choice(reproduction, p = [0.025, 0.025, 0.025, 0.025, 0.9])
			child_dormancy = np.random.normal(self.dormancy_time, 100)
			child = Agent(self.x, self.y, self.enviro, food_level = new_foodlevel, resistance = child_resistance, reproduction = child_reproduction, dormancy_time = child_dormancy)
			self.enviro.agents[self.key] = child
		self.reproduce_level = self.reproduce_level + (self.resistance * self.fitness_cost)

	def eat(self):
		for food in self.enviro.food:
			foodpos_x = food.x
			foodpos_y = food.y
			if 0.95 * food.size < np.sqrt((self.x - foodpos_x)**2 + (self.y - foodpos_y)**2) < 1 * 1.05 *food.size:
				self.food_level += 1.0
				#self.enviro.food[i].eaten(self)

	def neutralise(self,i):
		for antibiotic in self.enviro.antibiotics:
			antibiotics_x = antibiotic.x
			antibiotics_y = antibiotic.y
			anti_effect = antibiotic.effectiveness
			anti_halflife = antibiotic.halflife
			if  np.sqrt((self.x - antibiotics_x)**2 + (self.y - antibiotics_y)**2) < antibiotic.size:
				if i not in self.enviro.dead_key:
					self.enviro.dead_key.append(i)
					print("NEUTRALISE", i)

	def dormancy(self, i, dormancy_time):
		if self.enviro.time_ms - self.enviro.tbirths[-1] <= dormancy_time:
			self.enviro.agents[i].speed = 0
			self.enviro.agents[i].colour = (255,0,0)
			#self.agents[i].dormancy(0.9) #probability, time
		else:
			#print ("A")
			self.enviro.agents[i].speed = 2	
			self.enviro.agents[i].colour = (0,0,0)

	def die(self):
		self.enviro.remove_agent(self.key)
