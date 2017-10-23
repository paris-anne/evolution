import numpy as np
import environment as enviro
import particle as p

class Agent(p.Particle):
	def __init__(self, reproduce, environment):
		self.key = key
		self.food_level = food_level
		self.reproduce = reproduce
		self.enviro = environment

	def reproduce(self):
		self.food_level = self.food_level / 2.0
		child = Agent(self.reproduce, self.enviro)
		self.enviro.particles.append(child)
		self.enviro.add_agent(self.x, self.y, self.size, self.speed)

	def eat(self):
		# foodpos_x = p.Food(1).x
		# foodpos_y = p.Food(1).y
		foodpos_x = 0.5 * enviro.width()
		foodpos_y = 0.5 * enviro.height()
		for i in range(enviro.particles_list()):
			particles = enviro.particles_list()
			if np.sqrt((particles[i].x - foodpos_x)**2 + (particles[i].y - foodpos_y)**2)< p.Food.size:
				self.food_level += 0.1

	def die(self):
		self.enviro().remove_ag(key)