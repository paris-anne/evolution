import numpy as np
import random


class Environment:
	"""Create environment for agents to interact in """
	def __init__(self, numagents, numfood, width = 10, height = 10):
		self.__width  = width
		self.__height = height
		self.__numfood = numfood
		self.__numagents = numagents
		self.__foodslist = foods
		self.__agentslist = agents

	def maxposy(self):
		return self.__height

	def maxposx(self):
		return self.__width

	def plotdimensions(self):
		return np.array[self.__width, self.__height]

	def add_ag(self, key):
		return agents.append(key)

	def remove_ag(self,key):



	def food(self):
		return self.__food

	def addfood(self, number):
		food = np.zeros((self.__width, self.__height))
	

		newfood =[]
		for i in range(number):
			newfood.append((np.random.random_integers(0,height),(np.random.random_integers(0,width))))

		#newfood = [(3,2), (3,3)]
		#for i in range(len(newfood)):
		#	row = newfood[i][0] 
		#	column = newfood[i][1]
		#	food[row][column] += 1

	def removefood(self,k):




		return food


