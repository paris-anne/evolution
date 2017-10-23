import pygame
import math
import environment as env

class Particle:
	def __init__(self, x, y, size):
		self.x = x
		self.y = y
		self.size = size
		self.colour = (0, 0, 255)
		self.thickness = 1
		self.speed = 1
		self.angle = math.pi/2

	def bounce(self, width, height):
		if self.x > width - self.size:
			self.x = 2*(width - self.size) - self.x
			self.angle = - self.angle

		elif self.x < self.size:
			self.x = 2*self.size - self.x
			self.angle = - self.angle
		if self.y > height - self.size:
			self.y = 2*(height - self.size) - self.y
			self.angle = math.pi - self.angle
		elif self.y < self.size:
			self.y = 2*self.size - self.y
			self.angle = math.pi - self.angle

	def move(self):
		self.x += math.sin(self.angle) * self.speed
		self.y -= math.cos(self.angle) * self.speed

	def display(self, screen):
		pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

	def increasefoodlevel(self):
    	foodpos_x = 0.5 * env.width()
    	foodpos_y = 0.5 * env.height()
    	for i in range(env.particles()):
        	particle = self(x,y, size)
        	if np.sqrt((particle.x - foodpos_x)**2 + (particle.y - foodpos_y)**2)< size:
            	particle.food_level += 0.1
    
class Food(Particle):
	def __init__(self, size):
		self.x = 0
		self.y = 0
		self.speed = 0