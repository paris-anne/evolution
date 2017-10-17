import numpy as np
import random

class Environment(object):
	"""Create environment for agents to interact in """
	def __init__(self, food_percentage, pos = [0,0]):
		self.__width  = 10
		self.__height = 10
		self.__food = self.addfood(food_percentage)

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

	def addfood(self, percentage):
		food = np.zeros((self.width(), self.width()))
		points = self.width() * self.height()
		foodpoints = np.round(points * (percentage/100))
		for i in range(1, foodpoints):
			np.random.choice(food) += 1
		return food