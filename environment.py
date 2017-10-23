import numpy as np
import random
import pygame
import random
import particle as p
import math

class Environment(object):
	"""Create environment for agents to interact in """
	def __init__(self, width, height, colour = (255,255,255)):
		self.width  = width
		self.height = height		
		self.particles = []
		self.agents = []
		self.colour = colour
		self.screen = pygame.display.set_mode((self.width, self.height))

	def addfood(self):
		food = np.zeros((self.width, self.height))
		newfood =[]
		number = np.round((self.height * self.width)*food_percentage)
		for i in range(number):
			newfood.append((np.random.random_integers(0,self.height),(np.random.random_integers(0,self__width))))
		for i in range(len(newfood)):
			row = newfood[i][0] 
			column = newfood[i][1]
			food[row][column] += 1

	def add_agent(self, x, y, size, speed):
		agent = p.Agent(x, y, size, speed)
		particle.angle = random.uniform(0, math.pi*2)
		self.particles.append(particle)
		
	def add_agents(self, number_of_agents = 10, size = 3, speed = 2):
		for i in range(number_of_particles):
			x = random.randint(size, self.width - size)
			y = random.randint(size, self.height - size)
			agent = p.Agent(x, y, size, speed)
			agent.angle = random.uniform(0, math.pi*2)
			self.agents.append(agent)

	def display(self):
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			self.screen.fill(self.colour)
			for particle in self.particles:
				particle.move()
				particle.bounce(self.width, self.height)
				particle.display(self.screen)

			pygame.display.flip()
