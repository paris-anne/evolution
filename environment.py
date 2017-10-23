

# class Environment:
# 	"""Create environment for agents to interact in """
# 	def __init__(self, numagents, numfood, width = 10, height = 10):
# 		self.__width  = width
# 		self.__height = height
# 		self.__numfood = numfood
# 		self.__numagents = numagents
# 		self.__foodslist = foods
# 		self.__agentslist = agents

import numpy as np
import random
import pygame
import random
import particle as p
import math

class Environment(object):
	"""Create environment for agents to interact in """
	def __init__(self, food_percentage, pos = [0,0], colour = (255,255,255)):
		self.__width  = 100
		self.__height = 100
		#self.__food = self.addfood(food_percentage)
		
		self.particles = []
		self.food = []
		self.colour = (255,255,255)
		self.screen = pygame.display.set_mode((self.__width, self.__height))

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
		return self.fonp.round(od

	def addfood(self, food_percentage):
		food = np.zeros((self.__width, self.__height))
	

		newfood =[]
		number = np.round((self.__height * self __width)*food_percentage)
		for i in range(number):
			newfood.append((np.random.random_integers(0,self__height),(np.random.random_integers(0,self__width))))

		# newfood = [(3,2), (3,3)]
		for i in range(len(newfood)):
			row = newfood[i][0] 
			column = newfood[i][1]
			food[row][column] += 1

	def create(self):
		self.screen.fill(self.colour)

	def add_particles(self, number_of_particles = 10, size = 3, speed = 2):
		for i in range(number_of_particles):
			x = random.randint(size, self.__width - size)
			y = random.randint(size, self.__height - size)
			particle = p.Particle(x, y, size)
			particle.angle = random.uniform(0, math.pi*2)
			
			self.particles.append(particle)
			particle.display(self.screen)

	def run(self):
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			self.screen.fill(self.colour)
			for particle in self.particles:
				particle.move()
				particle.bounce(self.__width, self.__height)
				particle.display(self.screen)

			pygame.display.flip()
>>>>>>> 7e054874a57e2d67323e3788acf1604fa65b92e3
