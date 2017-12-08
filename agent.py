import numpy as np
import environment as enviro
import particle as p
import random
import antibiotic as ant


class Agent(p.Particle):
	key = -1
	random = np.random.choice([0, 1], p = [0.9, 0.1])

	def __init__(self, reproduction, dormancy_time, dormancy_period, generation =1, x=0, y=0, environment=None, size = 3.0, colour = (0, 0,0), reproduce_level = 5.0,  food_level = float(2.0),
	 resistance = 0, dormancy_gene = 1):
		super().__init__(x, y, size, colour)
		self.generation = generation
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

	def __reduce__(self):
		return (self.__class__, (self.reproduction, self.dormancy_time, self.dormancy_period, self.generation))

	def reproduce(self):
		new_foodlevel = self.food_level/float(self.reproduction)
		new_reproduce_level = self.reproduce_level/np.sqrt(self.reproduction)
		self.food_level = new_foodlevel
		for i in range(int(self.reproduction)):

			child_resistance = np.random.choice([self.resistance, (1-self.resistance)], p = [0.95, 0.05])

			reproduction = [2.0, 4.0, 8.0, 16.0]
			reproduction.remove(self.reproduction)
			reproduction.append(self.reproduction)
			child_reproduction = np.random.choice(reproduction, p = [np.float(0.1/3), np.float(0.1/3), np.float(0.1/3), 0.9])
			dormancy_time_mutation = np.random.uniform(0,5000)
			child_dormancy_time = np.random.choice([self.dormancy_time, dormancy_time_mutation], p = [0.99, 0.01])

			dormancy_period_mutation = np.random.uniform(10000,40000) #this should be distribution but with constant probability?
			# dormancy_period.remove(self.dormancy_period)
			# dormancy_period.append(self.dormancy_period)
			child_dormancy_period = np.random.choice([self.dormancy_period, dormancy_period_mutation], p = [0.99, 0.01])
			child_generation=self.generation+1
			child = Agent(x=self.x, y=self.y, generation=child_generation, environment=self.enviro, food_level = new_foodlevel, resistance = child_resistance, 
				reproduction = child_reproduction, dormancy_time = child_dormancy_time, dormancy_period = child_dormancy_period)
			self.enviro.agents[self.key] = child
		self.reproduce_level = self.reproduce_level + (self.resistance * self.fitness_cost)


	def eat(self):
		for food in self.enviro.food:
			foodpos_x = food.x
			foodpos_y = food.y
			if 0.95 * food.size < np.sqrt((self.x - foodpos_x)**2 + (self.y - foodpos_y)**2) < food.size:
				print("eat")
				self.food_level += 0.2
				#self.enviro.food[i].eaten(self)

	def neutralise(self,i):
		if i not in self.enviro.dead_key:
			self.enviro.dead_key.append(i)

			print("NEUTRALISE", i)

	def dormancy(self, i, dormancy_time):
		#print(dormancy_time, "dormancy_time")
		#print(self.enviro.time_ms, self.enviro.tbirths[-1])
		if self.enviro.time_ms == self.enviro.tbirths[-1] + 100:
			self.min_dist = self.enviro.agents[i].min_distance_antibiotic()

		speed_of_info = 0.01
		retarded_time = self.min_dist/speed_of_info


		if self.enviro.tbirths[-1] + retarded_time + dormancy_time >= self.enviro.time_ms >= self.enviro.tbirths[-1] + retarded_time:
			self.enviro.agents[i].speed = 0
			self.enviro.agents[i].colour = (255,0,0)

		else:

			self.enviro.agents[i].speed = 2	
			self.enviro.agents[i].colour = (0,0,0)
			self.min_distances = []


	def dormancy2(self, i, dormancy_period, dormancy_time):
		dormancy_period = dormancy_period - (dormancy_period%100)
		dormancy_time = dormancy_time - (dormancy_time%100)
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

