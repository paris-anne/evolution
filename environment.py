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

class Environment(object):
	"""Create environment for agents to interact in """
	def __init__(self, width = 100, height = 100, colour = (255,255,255)):
		self.width  = width
		self.height = height		
		self.colour = colour
		self.screen = pygame.display.set_mode((int(self.width), int(self.height)))
		self.food = []
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
		self.anti_conc = 0
		self.av_reproduction = []
		self.dead_key = []
		self.reproduce_key = []

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
	
	def addfood(self, food_coverage):
		amount = 0
		takeClosest = lambda num,collection:min(collection,key=lambda x:abs(x-num))
		squares = [1,4,9,16,25,36,49,64,81,100]
		amount = takeClosest(np.sqrt(self.area),squares)
		food_radius = np.sqrt((food_coverage*self.area)/(amount * math.pi))

		for i in np.arange(self.width/np.sqrt(amount), self.width, self.width/np.sqrt(amount)):
			for j in np.arange(self.height/np.sqrt(amount), self.height, self.height/np.sqrt(amount)):
				self.food.append(p.Particle(i, j, size = food_radius, speed = 0, colour = (139, 119, 101)))

	def add_agent(self, agent):
		self.agents[agent.key] = agent

	def add_agents(self, number_of_agents = 10, size = 3.0):
		for i in range(number_of_agents):
			x = random.randint(size, self.width - size)
			y = random.randint(size, self.height - size)
			agent = ag.Agent(x, y, self, size = size)
			self.agents[agent.key] = agent

	def remove_agent(self, key):
		del self.agents[key] 

	def add_antibiotics(self, concentration, frequency):
		amount = 0
		self.anti_freq = frequency
		self.anti_conc = concentration
		takeClosest = lambda num,collection:min(collection,key=lambda x:abs(x-num))
		squares = [1,4,9,16,25,36,49,64,81,100]
		amount = takeClosest(np.sqrt(self.area),squares)
		anti_radius = np.sqrt((concentration*self.area)/(amount * math.pi))

		for i in np.arange(self.width/np.sqrt(amount) + (self.width/np.sqrt(amount))/2 , self.width -(self.width/np.sqrt(amount))/2, self.width/np.sqrt(amount)):
			for j in np.arange(self.height/np.sqrt(amount) + (self.height/np.sqrt(amount))/2, self.height - (self.height/np.sqrt(amount))/2, self.height/np.sqrt(amount)):
				self.antibiotics.append(p.Particle(i, j, size = anti_radius, speed = 10, colour = (255, 100, 101)))


	def remove_antibiotics(self):
		self.antibiotics = []

	def display(self, time):
		reproduction_count = 0
		time_ms = 0
		running = True
		tbirths =[0]
		tdeaths = [0]
		t_betweenbirths = 5000
		t_lifetime = 200
		game_surf = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA, 32)
		pos = game_surf.get_rect()
		game_surf = game_surf.convert_alpha()
		for food in self.food: food.display(game_surf)
		while running:
			pygame.init()
			self.screen.fill(self.colour)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
			resistance = 0
			#for antibiotic in self.antibiotics:
			 #	antibiotic.display(game_surf)

			print(time_ms)
			if time_ms > time:
				running = False

			if time_ms-tbirths[-1] > self.anti_freq:
				self.add_antibiotics(self.anti_conc, self.anti_freq)
				tbirths.append(time_ms)
				#print ("a")

			if time_ms-tbirths[-1] > t_lifetime:
				#print("DEATH")
				self.antibiotics = []
			
			self.screen.fill(self.colour)
			reproduction = 0
			for i in self.agents: 
				print(self.agents[i].resistance)
				tbirths.append(time_ms)
				print ("a")
			self.screen.fill(self.colour)
			
			for i in self.antibiotics:
				i.display(self.screen)

			for i in self.agents: 
				#print(i)
				self.agents[i].display(self.screen)
				if self.agents[i].speed != 0:
					self.agents[i].move()
					self.agents[i].bounce(self.width, self.height)
					self.agents[i].food_level -= 0.02
					self.agents[i].eat()
					if self.agents[i].food_level > self.agents[i].reproduce_level: 
						self.reproduce_key.append(i)
						reproduction_count += 1
					if self.agents[i].resistance ==0:
					 	self.agents[i].neutralise(i)
					if self.agents[i].food_level < 0.0:
						self.dead_key.append(i)
					resistance += self.agents[i].resistance
					reproduction += self.agents[i].reproduction
			print(self.reproduce_key)
			print(self.dead_key)

			#print(reproduce_key)
			#res(dead_key)
			#print(resistance)
			if self.reproduce_key:
				for j in self.reproduce_key:
					self.agents[j].reproduce()
			if self.dead_key:
				for k in self.dead_key:
					self.dead.append(self.agents[k])
					del self.agents[k]
			self.reproduce_key = []
			self.dead_key = []
			self.screen.blit(game_surf, pos)
			pygame.display.flip()
			pop = len(self.agents)-len(self.dead) #becomes negative because only keeping alives agents in dict
			print(pop)
			time_ms+=300
			if pop != 0:
				self.time_elapsed.append(time_ms)
				self.deadcount.append(len(self.dead)/(time_ms))
				self.resistance.append(resistance)
				self.reproduction_rate.append(reproduction_count/(time_ms))
				self.alive.append(pop)
				self.av_resistance.append(resistance/pop)
				self.av_reproduction.append(reproduction/pop)
			else:
				running = False
		data = pd.DataFrame.from_items([('Time Elapsed', self.time_elapsed), ('Population', self.alive), ('Deadcount', self.deadcount), ('Reproduction', self.reproduction_rate), ('Resistance', self.av_resistance), ('Reproduction Count', self.av_reproduction)])
		return data
