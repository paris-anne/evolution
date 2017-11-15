import matplotlib.pyplot as pl
import pandas as pd 

def plot(dataframe):
		ax1 = pl.subplot(511)
		pl.plot(dataframe['Time Elapsed'], dataframe['Population'])
		ax1.title.set_text("Population") # add caption
		pl.setp(ax1.get_xticklabels(), fontsize=6)
		ax2 = pl.subplot(512, sharex=ax1) 
		ax2.title.set_text("Death Rate")
		pl.plot(dataframe['Time Elapsed'], dataframe['Deadcount'])		
		pl.setp(ax2.get_xticklabels(), visible=False)
		ax3 = pl.subplot(513, sharex=ax1)
		ax3.title.set_text("Reproduction Rate")
		pl.plot(dataframe['Time Elapsed'], dataframe['Reproduction'])
		ax4 = pl.subplot(514, sharex=ax1)
		pl.plot(dataframe['Time Elapsed'], dataframe['Resistance'])
		pl.setp(ax3.get_xticklabels(), visible=False)
		ax4.title.set_text("Resistance")
		ax5 = pl.subplot(515, sharex=ax1)
		pl.plot(dataframe['Time Elapsed'], dataframe['Reproduction Count'])
		pl.setp(ax4.get_xticklabels(), visible=False)
		ax5.title.set_text("Reproduction Count")
		pl.show()
		pl.savefig('plots.png')