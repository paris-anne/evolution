import numpy as np
import random
import pygame
import random
import particle as p
import antibiotic as ant
import agent as ag
import matplotlib.pyplot as pl
import matplotlib.animation as animation
import math
import pandas as pd
import food as f
import math
import plots

class Environment(object):
    def __init__(self, width = 100, height = 100, colour = (255,255,255)):
        self.width  = width
        self.height = height     
        self.area = self.width * self.height   
        self.colour = colour
        self.screen = pygame.display.set_mode((int(self.width), int(self.height)))

        self.food = []#{}
        self.agents = {}

        self.time_elapsed =[]

        self.population_count = []
        self.dormancy_count = []
        self.resistant_count = []
        self.reproduction_rate = []
        self.av_resistance = np.divide(self.resistant_count, self.population_count)
        self.avnumberdormant = np.divide(self.dormancy_count, self.population_count)
        self.av_reproduction = []
        self.av_dormancy_time = []

        self.deathsbyfood = []
        self.deathsbyanti = []
        self.deathsbyimmune = []
        # self.deathstotal = [0,0,0,0,0] + np.add(np.add(self.deathsbyfood, self.deathsbyanti), self.deathsbyimmune)

        self.antibiotics = []
        self.anti_freq = 0
        self.anti_conc = []
        self.tbirths = 0
        self.time_ms = 0
        self.antibiotics_count = 1

        self.immune_system = 2400
        self.killfrac = 0.0#0.1

        self.skipped_doses = []
        self.double_doses = []
        self.numberofdoses = 100
        self.generations = []

        self.hist_data = []
        self.hist_freq = 1000
        self.hist_offspring = []
        self.offspring_list = []
        self.hist_dormancy_time = []
        self.dormancy_time_list = []
        self.hist_dormancy_freq = []
        self.dormancy_freq_list = []
        self.hist_dormancyfreqplustime = []
        self.dormancyfreqplustime_list = []
        self.plotlabel = 0

        self.reproduction_counter = [0]*1001
        self.reproduct_MA = []

        self.deaths_counter = [0] *1001
        self.deaths_MA = []

        self.dead_key = []

    def __reduce__(self):
        return (self.__class__, (self.deathsbyimmune, self.deathsbyanti, self.deathsbyfood, self.dormancy_count, self.hist_dormancy_time, self.hist_freq))
     
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

    def add_agents(self, number_of_agents = 10, size = 3.0):
    	for i in range(number_of_agents):
    		offspring_dict = {2:4, 4:6, 6:8, 8:10, 10:15, 2.5:4.5, 4.5:6.5, 6.5:8.5, 8.5:10.5, 10.5:15.5}
    		x = random.randint(size, self.width - size)
    		y = random.randint(size, self.height - size)
    		reproduction = np.random.choice([2.0, 4.0, 6.0, 8.0, 10.0],  p = [0.9, np.float(0.1)/4, np.float(0.1)/4, np.float(0.1)/4, np.float(0.1)/4])         
    		agent = ag.Agent(reproduction = reproduction, dormancy_time = np.random.uniform(0,15000), dormancy_period = np.random.uniform(10000,40000), x=x, y=y, environment=self, size = size, 
    			resistance  = np.random.choice([0, 1], p = [1., 0.]), 
    			dormancy_gene = np.random.choice([0, 1], p = [0.9, 0.1]), reproduce_level=offspring_dict[reproduction]
    			)
    		self.agents[agent.key] = agent

    def remove_agent(self, key):
    	del self.agents[key]

    # def remove_agents_and_anti(self):
    #     self.agents={}
    #     self.antibiotics = []

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
    				self.antibiotics.append(ant.Antibiotic(i, j, size = 5))

    def set_first_dose(self, time):
        self.tbirths=time


    def set_anti_conc(self, conc):
        self.anti_conc = conc

    def set_anti_halflife(self, halflife):
        self.anti_halflife = halflife

    def set_anti_freq(self, freq):
        self.anti_freq = freq

    def set_numberofdoses(self, numberofdoses):
        self.numberofdoses = numberofdoses

    def remove_antibiotics(self):
        self.antibiotics = []

    def set_skipped_doses(self, doses):
        self.skipped_doses = doses

    def set_double_doses(self, doses):
        self.double_doses = doses

    def set_plotlabel(self,label):
        self.plotlabel = label

    def display(self, time, display):
        self.time_ms = 0
        self.antibiotics_count = 1
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
        # dataframes2 = []

        while running:
            #print((self.time_ms, len(self.agents)))
            print(self.av_resistance)
            food_amount = 0
            reproduction = 0
            resistance = 0
            dormant = 0
            deathsbyimmune = 0
            deathsbyanti = 0
            deathsbyfood = 0    
            dormancy_count = 0
            reproduction_counter = 0
            # resistant = pd.DataFrame()
            # agents = list(self.agents.values())
            # for i in agents:
            #     if i.resistance == 0:
            #         agents.remove(i)
            # resistant[self.time_ms] = pd.Series(agents)
            total = pd.DataFrame()
            total[self.time_ms]=pd.Series(list(self.agents.values()))
            #print(total)
            # dataframes.append(resistant)
            dataframes.append(total)

            if display == True:
                pygame.init()
                self.screen.fill(self.colour)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                for i in self.antibiotics:
                    i.display(self.screen)
                for i in self.agents: #include in main loop?
                    self.agents[i].display(self.screen)
                self.screen.blit(game_surf, pos)
                pygame.display.flip()

                if self.time_ms > time:
                	running = False

            #for i in self.food:
             #  self.food[i].display(self.screen)
             #  food_amount += self.food[i].size*self.food[i].size
            # for i in self.antibiotics:
            #   i.display(self.screen)

            for i in self.antibiotics:
                i.effectiveness = (np.e)**(-(self.time_ms-self.tbirths)/self.anti_halflife)
                if i.effectiveness < (np.e)**(-(self.anti_freq)/self.anti_halflife)  :
                    self.antibiotics.remove(i)

            if self.time_ms == self.tbirths:
                self.add_antibiotics(double_dose = False)

            if self.antibiotics_count < self.numberofdoses:
                if self.time_ms-self.tbirths >self.anti_freq:
                    tnextbirth = self.tbirths + self.anti_freq
                    self.tbirths = tnextbirth
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
                    self.antibiotics_count += 1

            if (self.time_ms%self.immune_system) == 0:

                killfrac = self.killfrac
                # numberkill = math.floor(killfrac*len(self.agents))
                # remainder = len(self.agents)*killfrac - numberkill
                # remainder = round(remainder, 1)
                # numberkill += np.random.choice((1,0), p = [remainder, 1 - remainder])

                # for i in range(numberkill):
                #     if self.agents:
                #         del self.agents[random.choice(list(self.agents.keys()))]
                #         deathsbyimmune += 1

                for i in range(math.ceil(killfrac*len(self.agents))):
                    if self.agents:
                        del self.agents[random.choice(list(self.agents.keys()))]
                        deathsbyimmune += 1
            
            resistant_agents=[]
            self.dead_key=[]
            reproduce_key =[]
            
            #change looping to list of agents.apply???
            if self.agents:
                for i in self.agents: 
                    self.generations.append(self.agents[i].generation)
                    self.offspring_list.append(self.agents[i].reproduction)
                    self.dormancy_time_list.append(self.agents[i].dormancy_time)
                    self.dormancy_freq_list.append(self.agents[i].dormancy_period)
                    self.dormancyfreqplustime_list.append(self.agents[i].dormancy_time + self.agents[i].dormancy_period)
                    if self.agents[i].resistance == 1:
                    	self.agents[i].colour = (0,0,255)
                    	resistant_agents.append(self.agents[i])
                    else:
                    	self.agents[i].colour = (0,0,0)
                    #self.agents[i].dormancy2(i, self.agents[i].dormancy_period ,self.agents[i].dormancy_time) # time between dormancies, time of dormancy
                    resistance += self.agents[i].resistance
                    dormant +=self.agents[i].dormancy_gene
                    if self.agents[i].dormancy_gene == 1:
                    	self.agents[i].dormancy(i, self.agents[i].dormancy_time)
                        #self.agents[i].dormancy2(i,self.agents[i].dormancy_time, self.agents[i].dormancy_period)
                    if self.agents[i].speed == 0:
                    	self.agents[i]. colour = (255,0,0)
                    	dormancy_count+=1
                    else:
                        self.agents[i].move()
                        self.agents[i].bounce(self.width, self.height)
                        self.agents[i].food_level -= 0.005 #move
                        self.agents[i].eat()
                        if self.agents[i].food_level > self.agents[i].reproduce_level: 
                            reproduce_key.append(i)
                            reproduction_count += 1
                        #print(self.antibiotics[0].effectiveness)
                        #print(self.agents[i].dormancy_time)
                        if self.agents[i].food_level < 0.00:
                            if i not in self.dead_key:
                                self.dead_key.append(i)
                                deathsbyfood += 1
                    for antibiotic in self.antibiotics:
                        antibiotics_x = antibiotic.x
                        antibiotics_y = antibiotic.y
                        anti_effect = antibiotic.effectiveness
                        anti_halflife = antibiotic.halflife
                        if  np.sqrt((self.agents[i].x - antibiotics_x)**2 + (self.agents[i].y - antibiotics_y)**2) < antibiotic.size:
                            if self.agents[i].resistance == 0:
                            	kill = np.random.choice([True,False], p=[self.antibiotics[0].effectiveness, (1-self.antibiotics[0].effectiveness)])
                            	if kill==True:
                            		self.agents[i].neutralise(i)
                            		deathsbyanti += 1
            if reproduce_key:
            	for j in reproduce_key:
            		if j in self.agents.keys():
            			offspring = self.agents[j].reproduce()
            			reproduction_counter += offspring

            if self.dead_key:
                for k in self.dead_key:
                    del self.agents[k]

            if self.time_ms% self.hist_freq == 0:
                self.hist_data.append((self.generations, self.time_ms))
                self.hist_offspring.append((self.offspring_list, self.time_ms))
                self.hist_dormancy_time.append((self.dormancy_time_list, self.time_ms))
                self.hist_dormancy_freq.append((self.dormancy_freq_list, self.time_ms))
                self.hist_dormancyfreqplustime.append((self.dormancyfreqplustime_list, self.time_ms))
            self.generations = []
            self.dormancy_time_list = []
            self.dormancy_freq_list = []
            self.offspring_list = []
            self.dormancyfreqplustime_list = []

            pop = len(self.agents)
            self.time_ms+=100

            for i in self.antibiotics:
            	if i.colour[0]<254 and i.colour[1]<254 and i.colour[2]<254:
            		i.colour = np.add(i.colour, (3,1,3))
            deathstotal = np.add(np.add(self.deathsbyfood, self.deathsbyanti), self.deathsbyimmune)

            if pop != 0:
            	self.time_elapsed.append(self.time_ms)
            	self.reproduction_rate.append(reproduction_count/(self.time_ms))
            	self.reproduction_counter.append(reproduction_counter)
            	self.population_count.append(pop)
            	self.resistant_count.append(float(resistance))
            	self.av_reproduction.append(reproduction/pop)
            	self.deathsbyimmune.append(deathsbyimmune)
            	self.deathsbyanti.append(deathsbyanti)
            	self.deathsbyfood.append(deathsbyfood)
            	self.dormancy_count.append(dormancy_count)
            	self.reproduct_MA.append(sum(self.reproduction_counter[-101:-1])/10000)
            	self.deaths_MA.append(sum(deathstotal[-101:-1])/10000)



            else:
                self.time_elapsed.append(self.time_ms)
                self.reproduction_rate.append(reproduction_count/(self.time_ms))
                self.reproduction_counter.append(reproduction_counter)
                self.population_count.append(pop)
                self.av_reproduction.append(0)
                self.resistant_count.append(float(resistance))
                self.deathsbyimmune.append(deathsbyimmune)
                self.deathsbyanti.append(deathsbyanti)
                self.dormancy_count.append(0)
                self.deathsbyfood.append(deathsbyfood)
                self.reproduct_MA.append(sum(self.reproduction_counter[-1001:-1])/100000)
                self.deaths_MA.append(-sum(deathstotal[-1001:-1])/100000)



            print(self.time_ms, pop)
            #print(sum(self.reproduction_counter[-5:-1]))





            #if self.antibiotics_count == self.numberofdoses:
            #   running = False
            #   print(self.antibiotics_count, "doses")
            #print(len(self.agents))
        #print(self.resistance)
        # dormancy_df = pd.DataFrame()
        # dormancy_df['time'] = pd.Series(self.time_elapsed)
        # dormancy_df['dormancy'] = pd.Series(self.dormancy_count)
        #print(self.reproduct_MA)
        #print(self.deaths_MA)

        self.av_resistance = np.divide(self.resistant_count, self.population_count)
        self.avnumberdormant = np.divide(self.dormancy_count, self.population_count)
        print(len(self.reproduction_counter[-5:-1]))
        # resistant = pd.concat(dataframes, axis=1)
        total=pd.concat(dataframes, axis=1)
        # pop=pd.DataFrame({"population" :total.count()})
        # respop=pd.DataFrame({"population" :resistant.count()})
        # pl.figure("reproduction")
        # pl.plot(self.time_elapsed, self.reproduct_MA, label = "reproduction rate")
        # pl.plot(self.time_elapsed, self.deaths_MA, label = "death rate")
        # pl.legend()
        # pl.grid(which = "both")


        # pl.figure("tot")
        # pl.plot(self.time_elapsed, np.subtract(self.reproduct_MA, self.deaths_MA))
        # pl.grid(which = "both")
        # #pl.show()
        # pl.figure("repr,pop")
        # pl.scatter(self.population_count, self.reproduct_MA, marker = '.')
        # slope, intercept = np.polyfit(self.population_count, self.reproduct_MA, 1)
        # pl.grid(which = "both")

        # print(slope,intercept)





        # #print(pop)
        # pl.figure("Deathsplot" + str(self.plotlabel))
        # pl.plot(self.time_elapsed, self.deathsbyimmune, 'r', label = "immune system")
        # pl.plot(self.time_elapsed, self.deathsbyanti, 'g', label = "antibiotics")
        # pl.plot(self.time_elapsed, self.deathsbyfood, 'b', label = "movement")
        # pl.title("Cause of Death")
        # pl.xlabel("Time Elapsed")
        # pl.ylabel("Frequency")
        # pl.legend()
        # pl.grid(True, which='both')
        # #pl.show()

        # pl.figure(2)
        # pl.plot(self.time_elapsed, self.av_resistance, label='Miss dose number: ' + str(self.plotlabel))
        # pl.title("Average resistance")
        # pl.xlabel("Time Elapsed")
        # pl.ylabel("Average resistance")
        # pl.legend()
        # pl.grid(True, which='both')


        # pl.figure("averageresistamce" +str(self.plotlabel))
        # pl.plot(self.time_elapsed, self.av_resistance)
        # pl.title("Average resistance")
        # pl.xlabel("Time Elapsed")
        # pl.ylabel("Average resistance")
        # pl.grid(True, which='both')



        # pl.figure("pop/res plot, individual, missing dose no " +str(self.plotlabel) )
        # pl.plot(self.time_elapsed, pop, label='Total Population')
        # pl.plot(self.time_elapsed, self.resistancepop, label = "'Resistant Population'")
        # pl.title("Population vs time")
        # pl.xlabel("Time Elapsed")
        # pl.ylabel("Population")
        # pl.grid(True, which='both')
        # pl.legend()

        # pl.figure("deathsplotcum " + str(self.plotlabel))
        # pl.plot(self.time_elapsed, self.deathsbyimmune, label = "immune system")
        # pl.plot(self.time_elapsed, self.deathsbyanti, label = "antibiotics")
        # pl.plot(self.time_elapsed, self.deathsbyfood, label = "movement")
        # pl.title("Cumulative Cause of Death")
        # pl.xlabel("Time Elapsed")
        # pl.ylabel("Frequency")
        # pl.grid(True, which='both')
        # pl.legend()

        # pl.figure(100 )
        # pl.plot(self.time_elapsed, pop, label='Miss dose number: ' + str(self.plotlabel))
        # pl.title("Population vs time")
        # pl.xlabel("Time Elapsed")
        # pl.ylabel("Population")
        # pl.grid(True, which='both')
        # pl.legend()

        # pl.figure("number dormant")
        # pl.plot(self.time_elapsed, self.avnumberdormant, label = "dormant pop")
        # pl.title("dormant")



        # print(self.time_ms)
        # plots.dormancytime_hist(self.hist_dormancy_time, self.time_ms/self.hist_freq)
        #plots.dormancyfreq_hist((self.hist_dormancy_freq, self.hist_dormancy_time), self.time_ms/self.hist_freq)
        # plots.dormancyfreqplustime_hist(self.hist_dormancyfreqplustime , self.time_ms/self.hist_freq)
        #plots.generations_hist(data = (self.hist_dormancy_time, self.hist_dormancy_freq), frames =  self.time_ms/self.hist_freq)
        # return ["resistant", total, dormancy_df]
        return total
