import matplotlib as pl
import pandas as pd 

def plot_resistance(dataframe):
	x, y = dataframe['Time Elapsed'], dataframe['Resistance']
	pl.plot(x,y)
	pl.show