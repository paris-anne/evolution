import agent as ag
import numpy as np
import environment as env
import matplotlib.pyplot as pl
import datetime
import numpy as np
import random
import particle as p
import plots
import food as f 
import pandas as pd
 
# pre antibiotics & normal amount of bacteria - 50 agents, immune system 3000, 10%, 1200000 time
# working antibiotics: antibiotics(0.1, 43200, 14400); agents = 250

enviro = plots.run(first_dose = 0, anti_conc = 0.01, anti_freq = 10000, anti_halflife = 5000, skipped_doses = [] , double_doses = [], numberofdoses = 50, numberofagents = 500, plotlabel = None) #first dose, anti_conc,
