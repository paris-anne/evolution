import numpy as np
import random
import pygame
import random
import particle as p
import agent as ag
import math

class Environment(object):
	"""Create environment for agents to interact in """
	def __init__(self, colour = (255,255,255)):
		self.__width  = 100
		self.__height = 100		
		self.particles = []
		self.colour = (255,255,255)
		self.screen = pygame.display.set_mode((self.__width, self.__height))

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

	def addfood(self):
		food = p.Food(1) #size = 1
		self.particles.append(food)

	def add_agent(self, x, y, size, speed):
		agent = ag.Agent(x, y, size, speed)
		agent.angle = random.uniform(0, math.pi*2)
		self.particles.append(agent)
		
	def add_agents(self, number_of_agents = 10, size = 3, speed = 2):
		for i in range(number_of_particles):
			x = random.randint(size, self.width - size)
			y = random.randint(size, self.height - size)
			agent = ag.Agent(x, y, size, speed)
			agent.angle = random.uniform(0, math.pi*2)
			self.particles.append(agent)

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
