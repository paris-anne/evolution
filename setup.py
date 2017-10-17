import pygame
import random
import particle as p
import math

width, height = (300, 200)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('evolution')
background_colour = (255,255,255)
#all changes must be made before flip()
screen.fill(background_colour)

number_of_particles = 10
my_particles = []

for n in range(number_of_particles):
	size = random.randint(10, 20)
	x = random.randint(size, width - size)
	y = random.randint(size, height - size)
	
	particle = p.Particle(x, y, size)
	particle.speed = random.random()
	particle.angle = random.uniform(0, math.pi*2)
	
	my_particles.append(particle)
	particle.display(screen)

pygame.display.flip()

running = True
while running:
  for event in pygame.event.get():
  	for particle in my_particles:
  		particle.move()
  		particle.bounce(width, height)
  		particle.display(screen)
  		pygame.display.flip()
  	if event.type == pygame.QUIT:
  		running = False