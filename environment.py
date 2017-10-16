import numpy as np
import random

class Environment(object):
	"""Create environment for agents to interact in """
	def __init__(self, pos = [0,0]):
		self.__width  = 10
		self.__height = 10
		self.__food = self.addfood(0.1)

	def pos(self):
		return self.pos

	def maxposw(self):
		return np.abs(self.__width)

	def maxposh(self):
		return np.abs(self.__height)


	def plotdimensions(self):
		return np.array[self.__width, self.__height]

	def food(self):
		return self.__food

	def addfood(self, percentage):
		food = np.zeros(self.__width, self.width)
		points = self.__width * self.__height
		foodpoints = np.round(points * percentage)

		for i in range (1,foodpoints):
			np.random.choice(food)[np.random.randrange(len(choice))] += 1

		return food
