import pygame
import math
import random

class Particle:

	def __init__(self, x, y, size, colour = (0, 0, 255), speed = 1.0, thickness = 0):
		self.x = x
		self.y = y
		self.size = size
		self.colour = colour
		self.thickness = thickness
		self.speed = speed
		self.angle = random.uniform(0, math.pi*2)

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

	# should a decrease of food happen in this method (tricky as refers to child class field) 
	def move(self):
		self.x += math.sin(self.angle) * self.speed
		self.y -= math.cos(self.angle) * self.speed

	def display(self, screen):
		pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), int(self.size), self.thickness)
