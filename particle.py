import pygame
import math

class Particle:
	def __init__(self, x, y, size, speed):
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


	
class Food(Particle):
	def __init__(self, size):
		self.x = 50
		self.y = 50
		self.speed = 0
		self.colour(255,0,0)
		self.size = size

	def set_x(self):
		return self.x = x
		
	def set_y(self):
		return self.y = y