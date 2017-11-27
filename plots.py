import matplotlib.pyplot as pl
import pandas as pd 
from scipy.optimize import curve_fit
import numpy as np
from scipy.integrate import odeint


def plot(dataframe):
		ax1 = pl.subplot(511)
		pl.plot(dataframe.loc(0), dataframe['Population'])
		ax1.title.set_text("Population") # add caption
		pl.plot(dataframe['Time Elapsed'], dataframe["Population"])
		pl.setp(ax1.get_xticklabels(), fontsize=6)
		ax2 = pl.subplot(412, sharex=ax1) 
		ax2.title.set_text("Death Rate")
		pl.plot(dataframe['Time Elapsed'], dataframe['Deadcount'])		
		pl.setp(ax2.get_xticklabels(), visible=False)
		ax3 = pl.subplot(413, sharex=ax1)
		ax3.title.set_text("Reproduction Rate")
		pl.plot(dataframe['Time Elapsed'], dataframe['Reproduction'])
		# ax4 = pl.subplot(514, sharex=ax1)
		# pl.plot(dataframe['Time Elapsed'], dataframe['Resistance'])
		# pl.setp(ax3.get_xticklabels(), visible=False)
		# ax4.title.set_text("Resistance")
		# ax5 = pl.subplot(515, sharex=ax1)
		# pl.plot(dataframe['Time Elapsed'], dataframe['Reproduction Count'])
		# pl.setp(ax4.get_xticklabels(), visible=False)
		# ax5.title.set_text("Reproduction Count")
		ax4 = pl.subplot(414)
		ax4.title.set_text("Food Population")
		pl.plot(dataframe['Time Elapsed'], dataframe['Food Population'])
		pl.savefig('plots.png')
		pl.show()

def func(x, a, c, d):
    return a*np.exp(c*x)+d

def LotkaVolterra(state,t):
  #x = state[0]
  y = state[0]
  alpha = 0.
  beta =  0.
  sigma = .001154
  gamma = 0.00008365
  #xd = x*(alpha - beta*y)
  yd = -y*(gamma - sigma*0.1)
  return [yd]

def LV_plots(dataframe):
	dataframe = dataframe.ix[:,1:-1]
	# t['time'] = dataframe.columns
	t=dataframe.count()
	df = pd.DataFrame(t.dropna())
	df.reset_index(level=0, inplace=True)	
	df.iloc[:,0] = pd.to_numeric(df.iloc[:,0], errors='coerce')
	t = df.iloc[:,0].values
	pop = df.iloc[:,1].values
	state0 = [20]
	state = odeint(LotkaVolterra, state0, t)
	# popt, pcov = curve_fit(func, list(dataframe), population.ix[0].tolist(), p0=(1, 1e-6, 1))
	# print(popt)
	food=[0.1] * len(df.ix[:,0].values)
	ax1 = pl.subplot(211)
	ax1.title.set_text("Bacteria Population")
	print(df.ix[:,0].values)
	pl.plot(t, pop)
	pl.plot(t, state)
	#pl.plot(list(dataframe), func(np.array(list(dataframe)), -1.71109885e-06, 4.26620601e-08, 2.00000017e+01))
	pl.setp(ax1.get_xticklabels(), visible=False)
	ax2 = pl.subplot(212, sharex=ax1)
	ax2.title.set_text("Food Concentration")
	pl.plot(df.ix[:,0].values, food)
	pl.setp(ax2.get_xticklabels(), fontsize=6)
	pl.savefig("LV_equations.png")
	pl.show()

def offspring_analysis(data):
	offspring = data.iloc[:, -1].apply(lambda x: x.reproduction if (np.all(pd.notnull(x))) else x)
	foodlevel = data.iloc[:, -1].apply(lambda x: x.food_level if (np.all(pd.notnull(x))) else x)
	merge = pd.concat([offspring, foodlevel], axis=1)
	merge.to_csv("offspring_v_foodlevel.csv")

def antibiotic_conc_v_population(data):
	population=pd.DataFrame(data.count())
	print(population)
	antibiotics=data.iloc[0,:].apply(lambda x: x.enviro.antibiotics[0].effectiveness)
	ax1 = pl.subplot(211)
	ax1.title.set_text("Bacteria Population")
	pl.plot(list(data), population.ix[:,0])
	pl.setp(ax1.get_xticklabels(), visible=False)
	ax2 = pl.subplot(212, sharex=ax1)
	ax2.title.set_text("Antibiotics Concentration")
	pl.plot(list(data), antibiotics)
	pl.setp(ax2.get_xticklabels(), fontsize=6)
	pl.savefig("antibiotics_bacteria.png")
	pl.show()	

def histogram(data):
	df = pd.DataFrame(data.iloc[:,-1])
	df = df.dropna()
	offspring = pd.DataFrame(data.iloc[:,-1].dropna().apply(lambda x: x.reproduction))
	dormancy = pd.DataFrame(data.iloc[:,-1].dropna().apply(lambda x: x.dormancy_time))
	print(offspring.iloc[:,0].values)
	pl.hist2d(offspring.iloc[:,0].values, dormancy.iloc[:,0].values, bins=50, cmap='Blues')
	cb = pl.colorbar()
	cb.set_label('counts in bin')
	pl.savefig("histogram.png")
	pl.show()
