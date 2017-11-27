import particle as p 

class Food(p.Particle):
	#key=0
	def __init__(self, x, y, environment, size = 3.0, colour = (139, 119, 101)):
		super().__init__(x, y, size, colour, speed = 0)
		self.enviro = environment
		self.x = x
		self.y = y
		self.colour = colour
		#Food.key+=1

	def eaten(self, agent):
		self.size = self.size - 0.1
		# if self.size < 0.1:
		# 	self.enviro.remove_food.append(self.key)
