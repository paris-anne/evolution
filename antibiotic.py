import numpy as numpy
import particle as p
import environment as enviro

class Antibiotic(p.Particle):
	count = 0


	def __init__(self, x, y, environment, size = 10.0, colour = (0, 255, 0), frequency = 2, deathage = 3):
		super().__init__(x, y, size, colour)
		self.key = self.count # need way of incrementing key
		self.size = size
		self.enviro = environment
		self.x = x
		self.y = y
		self.count +=1
		self.colour = colour
		self.frequency = frequency
		self.death_age = deathage
#		self.age = age

	def birth(self):
		self.enviro.antiobiotics.append(p)
	def death(self):
		if self.enviro.time_elapsed[-1] > death_time:
			self.colour = (255,255,255)

