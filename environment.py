import numpy as np
import random
import pygame
import random
import particle as p
import antibiotic as ant
import agent as ag
import matplotlib.pyplot as pl
import math
import pandas as pd
import food as f

class Environment(object):
	"""Create environment for agents to interact in """
	# np.random.seed(2)
	# random.seed(2)
	def __init__(self, width = 100, height = 100, colour = (255,255,255)):
		self.food_amount = 0
		self.width  = width
		self.height = height		
		self.colour = colour
		self.screen = pygame.display.set_mode((int(self.width), int(self.height)))
		self.food = []#{}
		self.agents = {}
		self.alive = []
		self.deadcount = []
		self.dead = []
		self.reproduction_rate = []
		self.time_elapsed =[]
		self.av_resistance = []
		self.population = 0
		self.resistance = []
		self.antibiotics = []
		self.antibiotics_effectiveness = 0
		self.anti_freq = 0
		self.area = self.width * self.height
		self.anti_conc = []
		self.av_reproduction = []
		self.dead_key = []
		self.reproduce_key = []
		self.food_pop = []
		self.remove_food = []
		self.tbirths = [0]
		self.time_ms = 0
		self.av_dormancy_time = []
		self.immune_system = 2000
		self.antibiotics_count = 0
		self.deathsbyfood = []
		self.deathsbyanti = []
		self.deathsbyimmune = []
		self.skipped_doses = []
		self.double_doses = []
		self.numberofdoses = 100
		self.dormancy_count = []

	def addfood(self, food_coverage):
		amount = 0
		takeClosest = lambda num,collection:min(collection,key=lambda x:abs(x-num))
		squares = [1,4,9,16,25,36,49,64,81,100]
		amount = takeClosest(np.sqrt(self.area),squares)
		food_radius = np.sqrt((food_coverage*self.area)/(amount * math.pi))

		for i in np.arange(self.width/np.sqrt(amount)/2, self.width + self.width/np.sqrt(amount)/2, self.width/np.sqrt(amount)):
			for j in np.arange(self.height/np.sqrt(amount)/2, self.height + self.width/np.sqrt(amount)/2, self.height/np.sqrt(amount)):
				food = f.Food(i, j, self, size = food_radius)
				self.food.append(food)
				# self.food[food.key] = food

	def add_agent(self, agent):
		self.agents[agent.key] = agent

	def set_first_dose(self, time):
		self.tbirths=[time]


	def set_anti_conc(self, conc):
		self.anti_conc = conc

	def set_anti_halflife(self, halflife):
		self.anti_halflife = halflife

	def set_anti_freq(self, freq):
		self.anti_freq = freq

	def set_numberofdoses(self, numberofdoses):
		self.numberofdoses = numberofdoses

	

	def add_agents(self, number_of_agents = 10, size = 3.0):
		for i in range(number_of_agents):
			offspring_dict = {2:5, 4:7, 6:9, 8:11, 10:17, 2.5:5.5, 4.5:7.5, 6.5:9.5, 8.5:11.5, 10.5:17.5}
			x = random.randint(size, self.width - size)
			y = random.randint(size, self.height - size)
			dormancy_time = np.random.uniform(0,5000)
			reproduction = np.random.choice([2.0, 4.0, 6.0, 8.0, 10.0],  p = [0.9, np.float(0.1)/4, np.float(0.1)/4, np.float(0.1)/4, np.float(0.1)/4])			
			agent = ag.Agent(reproduction = reproduction, dormancy_time = np.random.uniform(0,5000), dormancy_period = np.random.uniform(10000,40000), x=x, y=y, environment=self, size = size, 
				resistance  = np.random.choice([0, 1], p = [0.95, 0.05]), 
				dormancy_gene = np.random.choice([0, 1], p = [0.9, 0.1]), reproduce_level=offspring_dict[reproduction]
				)
			self.agents[agent.key] = agent

	def remove_agent(self, key):
		del self.agents[key]

	def remove_agents_and_anti(self):
		self.agents={}
		self.antibiotics = []


	def add_antibiotics(self, double_dose):
		amount = 0
		halflife = self.anti_halflife
		frequency = self.anti_freq
		if double_dose == True:
			concentration = 2 * self.anti_conc
		elif double_dose == False:
			concentration = self.anti_conc 
		takeClosest = lambda num,collection:min(collection,key=lambda x:abs(x-num))
		squares = [1,4,9,16,25,36,49,64,81,100]
		amount = takeClosest(np.sqrt(self.area),squares)
		anti_radius = np.sqrt((concentration*self.area)/(amount * math.pi))
		self.anti_radius = anti_radius

		for i in np.arange(0 , self.width +(self.width/np.sqrt(amount))/2, self.width/np.sqrt(amount)):
			for j in np.arange(0, self.height + (self.height/np.sqrt(amount))/2, self.height/np.sqrt(amount)):
				self.antibiotics.append(ant.Antibiotic(i, j, size = anti_radius))


	def remove_antibiotics(self):
		self.antibiotics = []

	def set_skipped_doses(self, doses):
		self.skipped_doses = doses

	def set_double_doses(self, doses):
		self.double_doses = doses


	def display(self, time, display):
		self.time_ms = 0
		self.antibiotics_count = 0
		reproduction_count = 0
		running = True
		if display == True:
			game_surf = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA, 32)
			pos = game_surf.get_rect()
			game_surf = game_surf.convert_alpha()
			for food in self.food: food.display(game_surf)
		#time_elapsed = [i for i in range(0, time, 300)]
		#data = pd.DataFrame(columns=pd.Series(time_elapsed))
		dataframes = []
		dataframes2 = []

		while running:
			print(self.time_ms, "time_ms")
			data = pd.DataFrame()
			data2 = pd.DataFrame()
			agents = list(self.agents.values())
			for i in agents:
				if i.resistance == 0:
					agents.remove(i)

			data[self.time_ms] = pd.Series(agents)
			data2[self.time_ms]=list(self.agents.values())			#data['resistance'] = pd.Series(list(self.av_resistance))

			#print(data)
			dataframes.append(data)
			dataframes2.append(data2)

			if display == True:
				pygame.init()
				self.screen.fill(self.colour)
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						running = False
				for i in self.antibiotics:
					i.display(self.screen)
				for i in self.agents: 
					self.agents[i].display(self.screen)
				self.screen.blit(game_surf, pos)
				pygame.display.flip()


			if self.time_ms > time:
				running = False
			food_amount = 0

			#for i in self.food:
			 #	self.food[i].display(self.screen)
			 #	food_amount += self.food[i].size*self.food[i].size
			# for i in self.antibiotics:
			# 	i.display(self.screen)

			reproduction = 0
			resistance = 0

			deathsbyimmune = 0
			deathsbyanti = 0
			deathsbyfood = 0	
			
			dormancy_count = 0
			for i in self.antibiotics:
				i.effectiveness = (np.e)**(-(self.time_ms-self.tbirths[-1])/self.anti_halflife)
				if i.effectiveness < (np.e)**(-(self.anti_freq)/self.anti_halflife)  :
					#print((np.e)**(-(self.anti_freq)/self.anti_halflife))
					self.antibiotics.remove(i)
					#print("deleted")

			if self.time_ms == self.tbirths[0]:
				self.add_antibiotics(double_dose = False)
				#print("first antbiotic added", self.time_ms)

			if self.time_ms-self.tbirths[-1] >self.anti_freq:
				tnextbirth = self.tbirths[-1] + self.anti_freq
				self.tbirths.append(tnextbirth)
				missed_doses = self.skipped_doses
				double_doses = self.double_doses

				if self.antibiotics_count not in missed_doses:
					#print(self.antibiotics_count + 1, "added")
					if self.antibiotics_count in double_doses:
						self.add_antibiotics(double_dose = True)
						#print("double_dose")
					elif self.antibiotics_count not in double_doses:
						#print("single_dose")
						self.add_antibiotics(double_dose = False)
					self.antibiotics[0].effectiveness = 1
					for i in self.antibiotics:
						i.colour = (0,255,0)

				#else:
					#print (self.antibiotics_count, "missed")
				self.antibiotics_count += 1

			#print(self.time_ms%6000)
			if (self.time_ms%self.immune_system) == 0:
				for i in range(int(0.1*len(self.agents))):
					if self.agents:
						del self.agents[random.choice(list(self.agents.keys()))]
						deathsbyimmune += 1

			for i in self.agents: 
				#change colour dep on resistance

				#print(self.agents[i].dormancy_time)
				# if self.agents[i].resistance == 1:
				# 	self.agents[i].colour = (0,0,255)
				# elif self.agents[i].resistance == 0:
				# 	self.agents[i].colour = (0,0,0)
				# #print(self.agents[i].food_level, "food_level")



				self.agents[i].dormancy2(i, self.agents[i].dormancy_period ,self.agents[i].dormancy_time) # time between dormancies, time of dormancy
				resistance += self.agents[i].resistance
				print(self.agents[i].reproduce_level, "reproduce")

				#print(self.time_ms%self.agents[i].dormancy_period, "remainder", self.agents[i].dormancy_time, "dorm time")
				if self.agents[i].speed == 0:
					dormancy_count+=1
				else:
					self.agents[i].move()
					self.agents[i].bounce(self.width, self.height)
					self.agents[i].food_level -= 0.01 #move
					self.agents[i].eat()
					if self.agents[i].food_level > self.agents[i].reproduce_level: 
						self.reproduce_key.append(i)
						reproduction_count += 1
					#print(self.antibiotics[0].effectiveness)
					#print(self.agents[i].dormancy_time)
					if self.agents[i].food_level < 0.00:
						self.dead_key.append(i)
						#print(i, "move")
						deathsbyfood += 1

					# #print(self.agents[i].reproduction)
					# reproduction += self.agents[i].reproduction#
			#print(resistance)
					for antibiotic in self.antibiotics:
						antibiotics_x = antibiotic.x
						antibiotics_y = antibiotic.y
						anti_effect = antibiotic.effectiveness
						anti_halflife = antibiotic.halflife
						#print(anti_effect, "halflife")
						if  np.sqrt((self.agents[i].x - antibiotics_x)**2 + (self.agents[i].y - antibiotics_y)**2) < antibiotic.size:
							if self.agents[i].resistance == 0:
								kill = np.random.choice([True,False], p=[self.antibiotics[0].effectiveness, (1-self.antibiotics[0].effectiveness)])
								if kill==True:
									self.agents[i].neutralise(i)
									deathsbyanti += 1
					#print(self.agents[i].dormancy_time)

			
			if self.reproduce_key:
				for j in self.reproduce_key:
					if j in self.agents.keys():
						self.agents[j].reproduce()
			if self.dead_key:
				for k in self.dead_key:
					del self.agents[k]
			# if self.remove_food:
			# 	for l in self.remove_food:
			# 		self.remove_food(l)
			self.reproduce_key = []
			self.dead_key = []
			# self.remove_food = []


				

			pop = len(self.agents)#-len(self.dead) #becomes negative because only keeping alives agents in dict
			self.time_ms+=100
			#print(len(self.agents))
			for i in self.antibiotics:
			 	if i.colour[0]<254:
			 		i.colour = np.add(i.colour, (3,0,0))
			#print(i.colour)
			if pop != 0:
				self.time_elapsed.append(self.time_ms)
				self.deadcount.append(len(self.dead)/(self.time_ms))
				self.resistance.append(resistance)
				self.reproduction_rate.append(reproduction_count/(self.time_ms))
				self.alive.append(pop)
				self.av_resistance.append(resistance/pop)
				self.av_reproduction.append(reproduction/pop)
				self.food_pop.append(food_amount)
				self.deathsbyimmune.append(deathsbyimmune)
				self.deathsbyanti.append(deathsbyanti)
				self.deathsbyfood.append(deathsbyfood)
				self.dormancy_count.append(dormancy_count)
			if pop ==0:
				self.time_elapsed.append(self.time_ms)
				self.deadcount.append(len(self.dead)/(self.time_ms))
				self.resistance.append(resistance)
				self.reproduction_rate.append(reproduction_count/(self.time_ms))
				self.alive.append(pop)
				self.av_resistance.append(0)
				self.av_reproduction.append(0)
				self.food_pop.append(food_amount)
				self.deathsbyimmune.append(deathsbyimmune)
				self.deathsbyanti.append(deathsbyanti)
				self.dormancy_count.append(dormancy_count)
				self.deathsbyfood.append(deathsbyfood)




			#if self.antibiotics_count == self.numberofdoses:
			#	running = False
			#	print(self.antibiotics_count, "doses")
			#print(len(self.agents))
		#print(self.resistance)
		dormancy_df = pd.DataFrame()
		dormancy_df['time'] = pd.Series(self.time_elapsed)
		dormancy_df['dormancy'] = pd.Series(self.dormancy_count)
		resistant = pd.concat(dataframes, axis=1)
		total=pd.concat(dataframes2, axis=1)

		pop=pd.DataFrame({"population" :total.count()})
		#print(data)
		#print(pop)
		pl.figure(1)
		pl.plot(self.time_elapsed, self.deathsbyimmune, 'r', label = "immune system")
		pl.plot(self.time_elapsed, self.deathsbyanti, 'g', label = "antibiotics")
		pl.plot(self.time_elapsed, self.deathsbyfood, 'b', label = "movement")
		pl.title("Causes of death")
		pl.xlabel("Time Elapsed")
		pl.ylabel("frequency")
		pl.legend()
		pl.grid(True)

		pl.figure(2)
		pl.plot(self.time_elapsed, self.av_resistance)
		pl.title("Average resistance")
		pl.xlabel("Time Elapsed")
		pl.ylabel("Average resistance")
		pl.grid(True)

		pl.figure(3)
		pl.plot(self.time_elapsed, pop)
		pl.title("Population vs time")
		pl.xlabel("Time Elapsed")
		pl.ylabel("Population")
		pl.grid(True)
		pl.show()

		return [resistant, total, dormancy_df]