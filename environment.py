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
		self.colour = colour
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.food 

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
		self.food = p.Particle(x, y, size, speed = 0, colour = (139, 119, 101)) #size = 1

	def add_agent(self, x, y, size, speed):
		agent = ag.Agent(x, y, self, size = size, speed = speed)
		agent.angle = random.uniform(0, math.pi*2)
		self.agents.append(agent)
		
	def add_agents(self, number_of_agents = 10, size = 3, speed = 2):
		for i in range(number_of_agents):
			x = random.randint(size, self.width - size)
			y = random.randint(size, self.height - size)
			agent = ag.Agent(x, y, self, size = size, speed = speed)
			agent.angle = random.uniform(0, math.pi*2)
			self.agents.append(agent)

#index will change as agents are removed therefore the key no longer matches up
	def remove_agent(self, key):
		self.agents.pop(key) #find better way of keeping data of dead agents whilst removing from screen

# current pygame functionality does not run on a loop therefore hard to iterate changes, 
# also does not have a time interval atm
	def display(self):
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				self.screen.fill(self.colour)
				self.food.display(self.screen)
			for agent in self.agents:
				#due to pygame set-up these conditions are currently only applied once at the 
				#start and do not interate
				if agent.food_level == 1.0: 
					agent.reproduce()
				if agent.food_level == 0.0:
					agent.die()
				agent.eat()
				agent.move()
				# should food_level be used up proportionally with speed or set at a constant?
				agent.food_level -= 0.1
				agent.bounce(self.width, self.height)
				agent.display(self.screen)

			pygame.display.flip()
