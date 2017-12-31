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

#SET DISPLAY LENGTH OF TIME IN THE PLOTS FILE & remember to change the dormancy method used to try each

#returns dataframe of all agents 
enviro = plots.run(first_dose = 0, anti_conc = 0.02, anti_freq = 10000, anti_halflife = 5000 , double_doses = [],skipped_doses = [], numberofdoses = 10, numberofagents = 200, plotlabel = None) #first dose, anti_conc,
plots.dormancytime_hist(enviro)

# # #plots.calibration()
# # #plots types of deaths by count
# # #
#plots.deaths(enviro)
#plots.reproductiondeathrates(enviro)

#plots.skip_two_doses(first_dose = 0, anti_conc = 0.02, anti_freq = 16000, anti_halflife = 4000 , double_doses = [], numberofdoses = 10, numberofagents = 500)
#plots.skip_one_dose(first_dose = 0, anti_conc = 0.02, anti_freq = 16000, anti_halflife = 4000 , double_doses = [], numberofagents = 500)

#plots population for antiobitics courses with length 1-10
#run for weak immune system too just change immune in environment
#plots.finish_early(first_dose = 0, anti_conc = 0.01, anti_freq = 16000, anti_halflife = 4000, skipped_doses = [] , double_doses = [], numberofagents = 500)

#loops through list missing more doses 
#plots.skip_doses(skip = [5,6,7,8], first_dose = 0, anti_conc = 0.01, anti_freq = 16000, anti_halflife = 4000, double_doses = [], numberofdoses = 10, numberofagents = 500)

#skips one dose, loops through position of skipped dose
# plots.skip_one_dose(first_dose = 0, anti_conc = 0.02, anti_freq = 16000, anti_halflife = 4000, double_doses = [], numberofdoses = 10, numberofagents = 500)
#plots.skip_three_doses(first_dose = 0, anti_conc = 0.02, anti_freq = 16000, anti_halflife = 4000 , double_doses = [], numberofdoses = 10, numberofagents = 500)


#number of dormant v time
#plots.dormancy_count(enviro)

#dormancy period histogram
#plots.dormancytime_hist(enviro)
pl.show()