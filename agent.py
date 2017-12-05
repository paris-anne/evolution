import numpy as np
import environment as enviro
import particle as p
import random
from collections import namedtuple

class Agent(p.Particle):
	key = -1
	random = np.random.choice([0, 1], p = [0.9, 0.1])
	def __init__(self, dormancy_time, reproduction, x = 0, y = 0, environment = None, size = 3.0, colour = (0, 0, 255), reproduce_level = 4.0,  food_level = float(2.0), resistance = 2, dormancy_gene = 1):
		super().__init__(x, y, size, colour)
		self.food_level = food_level
		self.fitness_cost = 1.0
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

	def __reduce__(self):
		return (self.__class__, (self.dormancy_time, self.reproduction))

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
			child = Agent(dormancy_time = child_dormancy, x = self.x, y=self.y, environment=self.enviro, food_level = new_foodlevel, resistance = child_resistance, reproduction = child_reproduction)
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
		min_dist = self.enviro.agents[i].min_distance_antibiotic()
		speed_of_info = 0.01
		retarded_time = min_dist/speed_of_info
		if min_dist < 20:
			retarded_time = 0

			if self.enviro.time_ms+retarded_time - self.enviro.tbirths[-1] <= dormancy_time:
				self.enviro.agents[i].speed = 0
				self.enviro.agents[i].colour = (255,0,0)
				#self.agents[i].dormancy(0.9) #probability, time
				#print("dormant")
			else:
			#print ("A")
				self.enviro.agents[i].speed = 2	
				self.enviro.agents[i].colour = (0,0,0)
				#print("not dormant")

	def min_distance_antibiotic(self):
		distances = []
		for antibiotic in self.enviro.antibiotics:
			antibiotics_x = antibiotic.x
			antibiotics_y = antibiotic.y
			#print(antibiotics_x, antibiotics_y)
			distances.append(np.sqrt((self.x - antibiotics_x)**2 + (self.y - antibiotics_y)**2))
		distances.sort()
		#print(len(distances))
		#print(min(distances))
		return min(distances)

	def die(self):
		self.enviro.remove_agent(self.key)

