import numpy as np
import random
import pygame
import random
import particle as p
import antibiotic as ant
import agent as ag
import matplotlib.pyplot as pl
import math
import pandas as pd

class Environment(object):
	"""Create environment for agents to interact in """
	def __init__(self, width = 100, height = 100, colour = (255,255,255)):
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
		self.antibiotics = []
		self.deadantibiotics =[]

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

	def food(self):
		return self.food

	def addfood(self, food_coverage):
		amount = 0
		area = self.width * self.height
		takeClosest = lambda num,collection:min(collection,key=lambda x:abs(x-num))
		squares = [1,4,9,16,25,36,49,64,81,100]
		amount = takeClosest(np.sqrt(area),squares)
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

	def add_antibiotics(self, concentration):
		amount = 0
		area = self.width * self.height
		takeClosest = lambda num,collection:min(collection,key=lambda x:abs(x-num))
		squares = [1,4,9,16,25,36,49,64,81,100]
		amount = takeClosest(np.sqrt(area),squares)
		anti_radius = np.sqrt((concentration*area)/(amount * math.pi))

		for i in np.arange(self.width/np.sqrt(amount), self.width, self.width/np.sqrt(amount)):
			for j in np.arange(self.height/np.sqrt(amount), self.height, self.height/np.sqrt(amount)):
				self.antibiotics.append(p.Particle(i, j, size = anti_radius, speed = 10, colour = (255, 100, 101)))

	def remove_antibiotics(self):
		self.antibiotics = []

	def display(self, time):
		reproduction_count = 0
		universal_clock = pygame.time.Clock()
		running = True
		tbirths =[0]
		tdeaths = [0]
		t_betweenbirths = 5000
		t_lifetime = 1000

		while running:
			pygame.init()
			self.screen.fill(self.colour)
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

			for food in self.food:
				food.display(self.screen)

			for agent in self.agents: 
				agent.display(self.screen)

			for antibiotic in self.antibiotics:
				antibiotic.display(self.screen)

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

			
			tbirths.append(tbirths[-1] + t_betweenbirths)
			tdeaths.append(tbirths[-1] + t_lifetime)
			#print (tbirths)
			


			for i in range(len(tbirths)):
				if tbirths[i] - 100 < time_ms < tbirths[i] + 100:
					print("a")
					tbirths.append(78000)
					tdeaths.append(tbirths[i] + t_lifetime)
					self.add_antibiotics(0.01)


			for i in range(len(tdeaths)):
				if tdeaths[i] - 100 <time_ms<tdeaths[i] + 100:
					self.antibiotics = []



			universal_clock.tick()
			universal_clock.get_time()
		data = pd.DataFrame.from_items([('Time Elapsed', self.time_elapsed), ('Population', self.population), ('Deadcount', self.deadcount), ('Reproduction', self.reproduction), ('Resistance', self.resistance)])
		return data

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