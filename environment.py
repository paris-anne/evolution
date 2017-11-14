import numpy as np
import random
import pygame
import random
import particle as p
import agent as ag
import matplotlib.pyplot as pl
import math
import pandas as pd

class Environment(object):
	"""Create environment for agents to interact in """
	def __init__(self, width, height, colour = (255,255,255)):
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

	def addfood(self):
		amount = 0
		food_coverage = 0.2
		area = self.width * self.height

		if area < 100:
			amount = 4
			food_radius = np.sqrt((food_coverage*area)/(amount * math.pi))
		elif area < 225:
			amount = 9
			food_radius = np.sqrt((food_coverage*area)/(amount * math.pi))
		elif area < 400:
			amount = 16
			food_radius = np.sqrt((food_coverage*area)/(amount * math.pi))
		elif area < 625:
			amount = 25
			food_radius = np.sqrt((food_coverage*area)/(amount * math.pi))
		elif area < 900:
			amount = 36
			food_radius = np.sqrt((food_coverage*area)/(amount * math.pi))
		elif area < 1600:
			amount = 49
			food_radius = np.sqrt((food_coverage*area)/(amount * math.pi))
		else:
			amount = 100
			food_radius = np.sqrt((food_coverage*area)/(amount * math.pi))

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

	def display(self, time):
		reproduction_count = 0
		clock = pygame.time.Clock()
		running = True
		game_surf = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA, 32)
		pos = game_surf.get_rect()
		game_surf = game_surf.convert_alpha()
		for food in self.food: food.display(game_surf)
		while running:
			pygame.init()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
			resistance = 0
			time_ms = pygame.time.get_ticks()
			if time_ms > time:
				running = False
			self.screen.fill(self.colour)
			dead_key = []
			reproduce_key = []
			for i in self.agents: 
				print(i)
				self.agents[i].display(self.screen)
				if self.agents[i].speed != 0:
					self.agents[i].move()
					self.agents[i].bounce(self.width, self.height)
					self.agents[i].food_level -= 0.01
					self.agents[i].eat()
					if self.agents[i].food_level > self.agents[i].reproduce_level: 
						reproduce_key.append(i)
						reproduction_count += 1
					if self.agents[i].food_level < 0.0:
						dead_key.append(i)
					resistance += self.agents[i].resistance
			print(reproduce_key)
			print(dead_key)
			if reproduce_key:
				for j in reproduce_key:
					self.agents[j].reproduce()
			if dead_key:
				for k in dead_key:
					self.dead.append(self.agents[k])
					del self.agents[k]
			reproduce_key = []
			dead_key = []
			self.screen.blit(game_surf, pos)
			pygame.display.flip()
			pop = len(self.agents)-len(self.dead)
			if pop != 0:
				self.time_elapsed.append(time_ms/1000)
				self.deadcount.append(len(self.dead)/(time_ms/1000))
				self.reproduction_rate.append(reproduction_count/(time_ms/1000))
				self.alive.append(pop)
				self.av_resistance.append(resistance/pop)
			else:
				running = False
			clock.tick()
			clock.get_time()
		data = pd.DataFrame.from_items([('Time Elapsed', self.time_elapsed), ('Population', self.alive), ('Deadcount', self.deadcount), ('Reproduction', self.reproduction_rate), ('Resistance', self.av_resistance)])
		return data
