import matplotlib.pyplot as pl
import pandas as pd 

def plot_resistance(dataframe):
	x, y = dataframe['Time Elapsed'], dataframe['Resistance']
	pl.plot(x,y)
	pl.show

def plot(dataframe):
		ax1 = pl.subplot(311)
		pl.plot(dataframe['Time Elapsed'], dataframe['Population'])
		ax1.title.set_text("Population") # add caption
		pl.setp(ax1.get_xticklabels(), fontsize=6)
		ax2 = pl.subplot(312, sharex=ax1) 
		ax2.title.set_text("Death Rate")
		pl.plot(dataframe['Time Elapsed'], dataframe['Deadcount'])		
		pl.setp(ax2.get_xticklabels(), visible=False)
		ax3 = pl.subplot(313, sharex=ax1)
		ax3.title.set_text("Reproduction Rate")
		pl.plot(dataframe['Time Elapsed'], dataframe['Reproduction'])
		pl.setp(ax3.get_xticklabels(), visible=False)
		pl.show()