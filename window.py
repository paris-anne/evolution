import pygame
import numpy as np
import random
import math

class Window:

	def __init__(self, background_colour = (255,255,255), width = 300, height = 200):
		self.background_colour = background_colour
		self.width = width
		self.height = height
		self.clock = pygame.time.Clock()
		

	def create(self, caption):
		screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption(caption)
		screen.fill(self.background_colour)
		pygame.display.flip()

		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

	def add_particles(self, number_of_particles = 10, size = 10):
		my_particles = []
		for n in range(number_of_particles):
			x = random.randint(size, self.width-size)
			y = random.randint(size, self.height-size)
			my_particles.append(Particle(self.x, self.y, size))
			particle.display()

		for particle in my_particles:
			particle.display()
		return