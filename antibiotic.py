import numpy as numpy
import particle as p
import environment as enviro

class Antibiotic(p.Particle):
	count = 0

	def __init__(self, x, y, size = 10000.0, colour = (0, 169, 0), effectiveness = 1, halflife = 3000, coordinates = []):
		super().__init__(x, y, size, colour)
		self.key = self.count # need way of incrementing key
		self.size = size
		self.x = x
		self.y = y
		self.count +=1
		self.colour = colour
		self.effectiveness = effectiveness
		self.halflife = halflife
		self.coordinates = coordinates
#		self.age = age


	def birth(self):
		self.enviro.antiobiotics.append(p)

	def death(self):
		if self.enviro.time_elapsed[-1] > death_time:
			self.colour = (255,255,255)

	def decayfactor(self, halflife, time_elapsed):
		self.effectiveness = (np.e)**(-time_elapsed/halflife)
		self.colour = np.add(self.colour, (5,0,5))
		return self.effectiveness
