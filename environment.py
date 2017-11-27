import numpy as np
import random
import pygame
import random
import particle as p
import antibiotic as ant
import agent as ag
import matplotlib.pyplot as pl
import math
import pandas as pd
import food as f

class Environment(object):
	"""Create environment for agents to interact in """
	def __init__(self, width = 100, height = 100, colour = (255,255,255)):
		self.food_amount = 0
		self.width  = width
		self.height = height		
		self.colour = colour
		self.screen = pygame.display.set_mode((int(self.width), int(self.height)))
		self.food = []#{}
		self.agents = {}
		self.alive = []
		self.deadcount = []
		self.dead = []
		self.reproduction_rate = []
		self.time_elapsed =[]
		self.av_resistance = []
		self.population = 0
		self.resistance = []
		self.antibiotics = []
		self.anti_freq = 0
		self.area = self.width * self.height
		self.anti_conc = []
		self.av_reproduction = []
		self.dead_key = []
		self.reproduce_key = []
		self.food_pop = []
		self.remove_food = []
		self.tbirths = [0]
		self.time_ms = 0
		self.av_dormancy_time = []
		self.immune_system = 3000

	def width(self):
		return self.width

	def set_width(self):
		self.width = width
		return

	def height(self):
		return self.height

	def set_height(self):
		self.height = height
		return

	def food(self):
		return self.food
	
	def remove_food(self, key):
		del self.food[key]


	def addfood(self, food_coverage):
		amount = 0
		takeClosest = lambda num,collection:min(collection,key=lambda x:abs(x-num))
		squares = [1,4,9,16,25,36,49,64,81,100]
		amount = takeClosest(np.sqrt(self.area),squares)
		food_radius = np.sqrt((food_coverage*self.area)/(amount * math.pi))

		for i in np.arange(self.width/np.sqrt(amount), self.width, self.width/np.sqrt(amount)):
			for j in np.arange(self.height/np.sqrt(amount), self.height, self.height/np.sqrt(amount)):
				food = f.Food(i, j, self, size = food_radius)
				self.food.append(food)
				# self.food[food.key] = food

	def add_agent(self, agent):
		self.agents[agent.key] = agent
#resistance = np.random.choice([0, 1], p = [0.1, 0.9]), 
	def add_agents(self, number_of_agents = 10, size = 3.0):
		for i in range(number_of_agents):
			x = random.randint(size, self.width - size)
			y = random.randint(size, self.height - size)
			agent = ag.Agent(x, y, self, size = size, reproduction = 2.0, dormancy_gene = np.random.choice([0, 1], p = [0.7, 0.3]), dormancy_time = np.random.choice([4000,5000,6000,7000,8000], p = [0.2,0.2,0.2,0.2,0.2]))
			self.agents[agent.key] = agent

	def remove_agent(self, key):
		del self.agents[key] 

	def add_antibiotics(self, concentration, frequency, halflife):
		amount = 0
		self.anti_halflife=halflife
		self.anti_freq = frequency
		self.anti_conc = concentration
		takeClosest = lambda num,collection:min(collection,key=lambda x:abs(x-num))
		squares = [1,4,9,16,25,36,49,64,81,100]
		amount = takeClosest(np.sqrt(self.area),squares)
		anti_radius = np.sqrt((concentration*self.area)/(amount * math.pi))

		for i in np.arange(self.width/np.sqrt(amount) + (self.width/np.sqrt(amount))/2 , self.width -(self.width/np.sqrt(amount))/2, self.width/np.sqrt(amount)):
			for j in np.arange(self.height/np.sqrt(amount) + (self.height/np.sqrt(amount))/2, self.height - (self.height/np.sqrt(amount))/2, self.height/np.sqrt(amount)):
				self.antibiotics.append(ant.Antibiotic(i, j, size = anti_radius))

	def remove_antibiotics(self):
		self.antibiotics = []

	def display(self, time):
		reproduction_count = 0
		running = True
		game_surf = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA, 32)
		pos = game_surf.get_rect()
		game_surf = game_surf.convert_alpha()
		for food in self.food: food.display(game_surf)
		#time_elapsed = [i for i in range(0, time, 300)]
		#data = pd.DataFrame(columns=pd.Series(time_elapsed))
		dataframes = []

		while running:
			data = pd.DataFrame()
			data[self.time_ms] = pd.Series(list(self.agents.values()))
			dataframes.append(data)
			pygame.init()
			self.screen.fill(self.colour)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
			resistance = 0
			# for antibiotic in self.antibiotics:
			#  	antibiotic.display(game_surf)
			#print(tbirths, "tbirths")
			if self.time_ms > time:
				running = False
			food_amount = 0
			# for i in self.food:
			# 	self.food[i].display(self.screen)
			# 	food_amount += self.food[i].size*self.food[i].size
			# for i in self.antibiotics:
			# 	i.display(self.screen)

			reproduction = 0
			self.screen.fill(self.colour)
			
			if self.antibiotics:
				for i in self.antibiotics:
					i.display(self.screen)

				if self.time_ms-self.tbirths[-1] >self.anti_freq:
					self.add_antibiotics(self.anti_conc, self.anti_freq, self.anti_halflife)
					tnextbirth = self.tbirths[-1] + self.anti_freq
					self.tbirths.append(tnextbirth)
					self.antibiotics[0].effectiveness = 1
					for i in self.antibiotics:
						i.colour = (0,255,0)
			
			if (self.time_ms%self.immune_system) == 0:
				for i in range(int(0.1*len(self.agents))):
					if self.agents:
						del self.agents[random.choice(list(self.agents.keys()))]

			for i in self.agents: 
				#print(i)
				self.agents[i].display(self.screen)
				#print(self.agents[i].dormancy_time)
				if self.antibiotics:
					self.agents[i].dormancy(i, self.agents[i].dormancy_time)
				if self.agents[i].speed != 0:
					self.agents[i].move()
					self.agents[i].bounce(self.width, self.height)
					self.agents[i].food_level -= 0.015 #move
					self.agents[i].eat()
					if self.agents[i].food_level > self.agents[i].reproduce_level: 
						self.reproduce_key.append(i)
						reproduction_count += 1
					if self.agents[i].resistance ==0:
						self.antibiotics[0].effectiveness = (np.e)**(-(self.time_ms-self.tbirths[-1])/self.anti_halflife)
						if self.antibiotics[0].effectiveness > np.random.uniform():
							self.agents[i].neutralise(i)
					#print(self.antibiotics[0].effectiveness)
					#print(self.agents[i].dormancy_time)
					if self.agents[i].food_level < 0.0:
						self.dead_key.append(i)
					# resistance += self.agents[i].resistance
					# #print(self.agents[i].reproduction)
					# reproduction += self.agents[i].reproduction
			
			if self.reproduce_key:
				for j in self.reproduce_key:
					self.agents[j].reproduce()
			if self.dead_key:
				for k in self.dead_key:
					del self.agents[k]
			# if self.remove_food:
			# 	for l in self.remove_food:
			# 		self.remove_food(l)
			self.reproduce_key = []
			self.dead_key = []
			# self.remove_food = []
			self.screen.blit(game_surf, pos)
			pygame.display.flip()
			pop = len(self.agents)-len(self.dead) #becomes negative because only keeping alives agents in dict
			self.time_ms+=100
			#print(len(self.agents))
			#for i in self.antibiotics:
			 	# i.colour = np.add(i.colour, (1,-1,1))
			 	# print(i.colour)
			if pop != 0:
			 	self.time_elapsed.append(self.time_ms)
			 	self.deadcount.append(len(self.dead)/(self.time_ms))
			 	self.resistance.append(resistance)
			 	self.reproduction_rate.append(reproduction_count/(self.time_ms))
			 	self.alive.append(pop)
			 	self.av_resistance.append(resistance/pop)
			 	self.av_reproduction.append(reproduction/pop)
			 	self.food_pop.append(food_amount)

			#print(len(self.agents))
	
		data = pd.concat(dataframes, axis=1)
		print(data)
		return data
