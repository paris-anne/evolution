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
		self.agents = []
		self.population = []
		self.deadcount = []
		self.dead = []
		self.reproduction = []
		self.time_elapsed =[]
		self.resistance = []

	def width(self):
		return self.width

	def set_width(self, width):
		self.width = width
		return

	def height(self):
		return self.height

	def set_height(self, height):
		self.height = height
		return

	def food(self):
		return self.food

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
		self.agents.append(agent)

	def add_agents(self, number_of_agents = 10, size = 3.0):
		for i in range(number_of_agents):
			x = random.randint(size, self.width - size)
			y = random.randint(size, self.height - size)
			agent = ag.Agent(x, y, self, size = size)
			self.agents.append(agent)

	def remove_agent(self, key):
		self.agents.pop(key) 

	def display(self, time):
		reproduction_count = 0
		clock = pygame.time.Clock()
		running = True
		while running:
			pygame.init()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
			resistance = 0

			for agent in self.agents:
				if agent.speed != 0:
					agent.eat()
					if agent.food_level > agent.reproduce_level: 
						agent.reproduce()
						reproduction_count += 1
					agent.move()
					agent.bounce(self.width, self.height)
					agent.food_level -= 0.01
					resistance += agent.resistance
					if agent.food_level < 0.0:
						agent.die()
			self.screen.fill(self.colour)
			for food in self.food: food.display(self.screen)
			for agent in self.agents: 
				agent.display(self.screen)
			pygame.display.flip()
			time_ms = pygame.time.get_ticks()
			if time_ms > time:
				running = False
			if (len(self.agents)-len(self.dead)) != 0:
				self.time_elapsed.append(time_ms/1000)
				self.deadcount.append(len(self.dead)/(time_ms/1000))
				self.reproduction.append(reproduction_count/(time_ms/1000))
				pop = len(self.agents)-len(self.dead)
				self.population.append(pop)
				self.resistance.append(resistance/pop)
			else:
				running = False
			clock.tick()
			clock.get_time()
		data = pd.DataFrame.from_items([('Time Elapsed', self.time_elapsed), ('Population', self.population), ('Deadcount', self.deadcount), ('Reproduction', self.reproduction), ('Resistance', self.resistance)])
		return data
