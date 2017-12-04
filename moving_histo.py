import pandas as pd 
import plotly.plotly as py
from plotly.grid_objs import Grid, Column
from plotly.tools import FigureFactory as FF 

import time

data = pd.DataFrame.from_csv("population.csv")
#df = data.dropna()

time_from_col = data.columnss
time = [str(time) for time in time_from_col]
keys = [i for i in range(data.shape[1])]

columns = []

for i in time:
	for key in keys:
		data_by_time = data[dataset['year'] == int(i)]
		data_by_time_count = data_by_time[data_by_time['agent'] = agent]

figure = {
	'data': [],
	'layout': {},
	'frames': [],
	'config': {'scollzoom': True}
}

figure['layout']['xaxis'] = {'range': [30, 85], 'title': 'Life Expectancy', 'gridcolor': '#FFFFFF'}
figure['layout']['yaxis'] = {'title': 'GDP per Capita', 'type': 'log', 'gridcolor': '#FFFFFF'}
figure['layout']['hovermode'] = 'closest'
figure['layout']['plot_bgcolor'] = 'rgb(223, 232, 243)'

figure['layout']['sliders] = {
	'active': 0,
	'yanchor': 'top',
	'xanchor': 'left',
	'currentvalue': {
		'font': {'size': 20},
		'prefix': 'text-before-value-on-display',
		'visible': True,
		'xanchor': 'right'
	},
	'transition': {'duration': 300, 'easing': 'cubic-in-out'},
	'pad': {'b': 10, 't': 50},
	'len': 0.9,
	'x': 0.1,
	'y': 0,
	'steps': [...]
	}
	


# offspring = pd.DataFrame(data.iloc[:,-1].dropna().apply(lambda x: x.reproduction))
# dormancy = pd.DataFrame(data.iloc[:,-1].dropna().apply(lambda x: x.dormancy_time))
# print(offspring.iloc[:,0].values)
# pl.hist2d(offspring.iloc[:,0].values, dormancy.iloc[:,0].values, bins=50, cmap='Blues')
# cb = pl.colorbar()
# cb.set_label('counts in bin')
# pl.savefig("histogram.png")
# pl.show()