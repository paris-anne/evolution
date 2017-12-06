import numpy as np
import environment as enviro
import particle as p
import random
import antibiotic as ant


class Agent(p.Particle):
	key = -1
	random = np.random.choice([0, 1], p = [0.9, 0.1])
	def __init__(self, x, y, environment, size = 3.0, colour = (0, 0, 255), reproduce_level = 4.0,  food_level = float(2.0),
	 resistance = 1, reproduction = 2, dormancy_gene = 1, dormancy_time = 700, dormancy_period = 1400):
		super().__init__(x, y, size, colour)
		self.food_level = food_level
		self.fitness_cost = 0.3
		self.size = size
		self.enviro = environment
		self.x = x
		self.y = y
		self.resistance = resistance
		self.reproduce_level = reproduce_level + (self.resistance * self.fitness_cost)
		self.reproduction = reproduction
		self.dormancy_gene = dormancy_gene
		self.dormancy_time = dormancy_time
		self.dormancy_period = dormancy_period
		self.min_dist = 100000

		#self.antibiotic_eff = ant.Antibiotic.effectiveness
		#self.dormancy_freq
		Agent.key += 1

	def reproduce(self):
		new_foodlevel = self.food_level/float(self.reproduction)
		self.food_level = new_foodlevel
		for i in range(int(self.reproduction)):
			child_resistance = np.random.choice([self.resistance, (1-self.resistance)], p = [1, 0])

			reproduction = [2.0, 3.0, 4.0, 5.0, 6.0]
			reproduction.remove(self.reproduction)
			reproduction.append(self.reproduction)
			child_reproduction = np.random.choice(reproduction, p = [0.0025, 0.0025, 0.0025, 0.0025, 0.99])


			dormancy_time = [2000,4000,6000,8000,10000]
			dormancy_time.remove(self.dormancy_time)
			dormancy_time.append(self.dormancy_time)
			child_dormancy_time = np.random.choice(dormancy_time, p = [0.025,0.025,0.025,0.025,0.9])

			dormancy_period = [2000,4000,6000,8000,10000, 12000,14000,16000,18000,20000,
							 22000,24000,26000,28000,30000,32000,34000, 36000, 38000,40000, 42000]
			dormancy_period.remove(self.dormancy_period)
			dormancy_period.append(self.dormancy_period)
			child_dormancy_period = np.random.choice(dormancy_period, p = [0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,
																	   0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,
																	   0.9])


			child = Agent(self.x, self.y, self.enviro, food_level = new_foodlevel, resistance = child_resistance, 
				reproduction = child_reproduction, dormancy_time = child_dormancy_time, dormancy_period = child_dormancy_period)
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
					#print("NEUTRALISE", i)

	def dormancy(self, i, dormancy_time):
		#print(dormancy_time, "dormancy_time")
		print(self.enviro.time_ms, self.enviro.tbirths[-1])
		if self.enviro.time_ms == self.enviro.tbirths[-1] + 100:
			self.min_dist = self.enviro.agents[i].min_distance_antibiotic()

		speed_of_info = 0.01
		retarded_time = self.min_dist/speed_of_info


		if self.enviro.tbirths[-1] + retarded_time + dormancy_time >= self.enviro.time_ms >= self.enviro.tbirths[-1] + retarded_time:
			self.enviro.agents[i].speed = 0.001
			self.enviro.agents[i].colour = (255,0,0)

		else:

			self.enviro.agents[i].speed = 2	
			self.enviro.agents[i].colour = (0,0,0)
			self.min_distances = []


	def dormancy2(self, i, dormancy_period, dormancy_time):
		if (self.enviro.time_ms%dormancy_period) == 0:
				self.enviro.agents[i].speed = 0
				self.enviro.agents[i].colour = (255,0,0)
		if (self.enviro.time_ms%dormancy_period) == dormancy_time:
				self.enviro.agents[i].speed = 2	
				self.enviro.agents[i].colour = (0,0,0)


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

