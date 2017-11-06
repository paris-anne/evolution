import numpy as np
import random
import pygame
import random
import particle as p
import agent as ag
import matplotlib.pyplot as pl
import math

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
		food_coverage = 0.1
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

	def add_agents(self, number_of_agents = 10, size = 3.0, speed = 2):
		for i in range(number_of_agents):
			x = random.randint(size, self.width - size)
			y = random.randint(size, self.height - size)
			agent = ag.Agent(x, y, self, size = size)
			self.agents.append(agent)

	def remove_agent(self, key):
		self.agents.pop(key) 

	# def livingpopulation(self):
	# 	self.livingpopulation.append(len(self.population) - len(self.deadpopulation))
	# 	return self.livingpopulation

# does not have a time interval atm
	def display(self, time):
		reproduction_count = 0
		clock = pygame.time.Clock()
		running = True
		while running:
			pygame.init()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False


			for agent in self.agents:
				if agent.speed != 0:
					agent.eat()
					if agent.food_level > agent.reproduce_level: 
						agent.reproduce()
						reproduction_count += 1
					agent.move()
					agent.bounce(self.width, self.height)
					agent.food_level -= 0.001
					if agent.food_level < 0.0:
						agent.die()
				
			self.screen.fill(self.colour)
			for food in self.food: food.display(self.screen)
			for agent in self.agents: 
				agent.display(self.screen)
			pygame.display.flip()
			time_ms = pygame.time.get_ticks()


			
			#print (time_ms)
			self.time_elapsed.append(time_ms/1000)
			self.population.append(len(self.agents)-len(self.dead))
			self.deadcount.append(len(self.dead)/(time_ms/1000))
			self.reproduction.append(reproduction_count/(time_ms/1000))
			if self.population[-1] == 0:
				running = False
				print("time to complete death: ", time_ms)

			if time_ms > time:
				running = False
				print("final population", len(self.population))
			clock.tick()
			print(clock.get_time())
			

			# pl.show()
			#main.Data.append((time_ms, len(self.agents)))

		

	def plot(self):
		ax1 = pl.subplot(311)
		pl.plot(self.time_elapsed, self.population)
		ax1.title.set_text("population") # add caption
		pl.setp(ax1.get_xticklabels(), fontsize=6)
		ax2 = pl.subplot(312, sharex=ax1) 
		ax2.title.set_text("death rate")
		pl.plot(self.time_elapsed, self.deadcount)		
		pl.setp(ax2.get_xticklabels(), visible=False)
		ax3 = pl.subplot(313, sharex=ax1)
		ax3.title.set_text("reproduction rate")
		pl.plot(self.time_elapsed, self.reproduction)
		pl.setp(ax3.get_xticklabels(), visible=False)
		pl.show()

