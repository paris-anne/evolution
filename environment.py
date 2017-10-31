import numpy as np
import random
import pygame
import random
import particle as p
import agent as ag
import math

class Environment(object):
	"""Create environment for agents to interact in """
	def __init__(self, width = 100, height = 100, colour = (255,255,255)):
		self.width  = width
		self.height = height		
		self.agents = []
		self.dead = []
		self.colour = colour
		self.screen = pygame.display.set_mode((int(self.width), int(self.height)))
		self.food = []
		self.population = []
		self.alive = []

	def particles_list(self):
		return self.particles

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

	def pos(self):
		return self.pos

	def maxposw(self):
		return np.abs(self.width())

	def maxposh(self):
		return np.abs(self.height())

	def plotdimensions(self):
		return np.array(self.width(), self.height())

	def food(self):
		return self.food

	def addfood(self, x, y, size):
		self.food.append(p.Particle(x, y, size, speed = 0, colour = (139, 119, 101)))

	def add_agent(self, agent):
		self.agents.append(agent)
	def add_agents(self, number_of_agents = 10, size = 3.0, speed = 1.0):
		for i in range(number_of_agents):
			x = random.randint(size, self.width - size)
			y = random.randint(size, self.height - size)
			agent = ag.Agent(x, y, self, size = size, speed = speed)
			self.agents.append(agent)

	def remove_agent(self, key):
		self.agents.pop(key) 

# does not have a time interval atm
	def display(self):
		clock = pygame.time.Clock()
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			for agent in self.agents:
				if agent.speed != 0:
					agent.eat()
					if agent.food_level > agent.reproduce_level: 
						agent.reproduce()
					agent.move()
					agent.bounce(self.width, self.height)
					agent.food_level -= 0.01
					if agent.food_level < 0.0:
						agent.die()
				
			self.screen.fill(self.colour)
			for food in self.food: food.display(self.screen)

			for agent in self.agents: 
				agent.display(self.screen)
			pygame.display.flip()
			population_toll = len(self.agents) - self.get_dead()
			self.population.append(population_toll) 
		clock.get_time()

	def get_dead(self):
		return len(self.dead)

	def get_population_time(self):
		return self.population
