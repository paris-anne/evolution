import agent as ag
import numpy as np
import environment as env
import matplotlib.pyplot as pl
import datetime
import numpy as np
import random
import plots
import particle as p

envirox = 200
enviroy = 200
enviro = env.Environment(envirox, enviroy)
enviro.addfood()
enviro.add_agents(20)
data = enviro.display(100000)
plots.plot(data)
