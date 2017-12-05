import pandas as pd
import numpy as np
import plotly as py
from plotly.tools import FigureFactory as ff 
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot

from plotly.grid_objs import Grid, Column
import plotly.graph_objs as go

dataframes = []

dataframe = pd.read_pickle("population.pkl").iloc[:,:-1]
#dataframe2 = pd.read_pickle("population.pkl").iloc[:,450:500]
#dataframe = pd.concat([dataframe1, dataframe2])
time = list(dataframe.columns)
print(time)
rep_bins = [i for i in np.arange(2.0, 6.0, 0.1)]
dorm_bins = [i for i in np.arange(3500.0, 9000.0, 100.0)]
# dataframe=dataframe.dropna()
#print(pd.DataFrame(dataframe.iloc[:,-1].dropna().apply(lambda x: x.dormancy_time)))
df = pd.DataFrame()
data = pd.DataFrame()
df = df.dropna()
# print(list(dataframe[104800].map(lambda x: x.dormancy_time if np.all(pd.notnull(x)) else x).values),
# )
def get_sliders(n_frames, fr_duration=1000, x_pos=0.0, slider_len=1.0):
    # n_frames= number of frames
    #fr_duration=the duration in milliseconds of each frame
    #x_pos x-coordinate where the slider starts
    #slider_len is a number in (0,1] giving the slider length as a fraction of x-axis length 
    return [dict(steps= [dict(method= 'animate',#Sets the Plotly method to be called when the slider value is changed.
                              args= [ [ '{}'.format(t) ],#Sets the arguments values to be passed to the Plotly,
                                                              #method set in method on slide
                                      dict(mode= 'immediate',
                                           frame= dict( duration=fr_duration, redraw= True ),
                                           transition=dict(duration= 0)
                                          )
                                    ],
                              label='{}'.format(t)
                             ) for t in time], 
                transition= { 'duration': 300 },
                x=x_pos,
                len=slider_len)]

def get_updatemenus(x_pos=0.0, fr_duration=1000):
    return [dict(x= x_pos,
                 y= 0,
                 yanchor='top',
                 xanchor= 'right',
                 pad= dict(r= 10, t=40 ),
                 type='buttons',
                 showactive= False,
                 buttons= [dict(label='Play',
                                method='animate',
                                args= [ None,
                                        dict(mode='immediate',
                                             transition= { 'duration': 100 },
                                             fromcurrent= True,
                                             frame= dict( redraw=True, duration=fr_duration)
                                            )
                                       ]
                                ),
                 dict(label='Pause',
                                method='animate',
                                args= [ [None],
                                        dict(mode='immediate',
                                             transition= { 'duration': 0 },
                                             frame= dict( redraw=True, duration=0 )
                                            )
                                       ]
                                       )
                           ]
               )
        ]

layout=dict(width=750, height=750,
            # font=dict(family='Balto', 
            #           size=12),

            xaxis= dict(range= [1.5,6.5], 
                        ticklen=4,  
                        autorange= False, 
                        zeroline=False, 
                        showline=True, 
                        mirror=True,
                        showgrid=True),
            yaxis=dict(range= [400, 1000], 
                       ticklen=4,  
                       autorange= False, 
                       showline=True, 
                       mirror=True,
                       zeroline=False, 
                       showgrid=True),
            plot_bgcolor = 'rgb(223, 232, 243)',
            title= 'Evolution', 
            hovermode='closest',
            sliders=get_sliders(n_frames=len(time)),
            updatemenus=get_updatemenus()
            )
# for t in list(dataframe.columns):

# 	#df[column] = data[column].dropna()
# 	# print(df[column])
# 	df['{time}_{gene}'.format(time=t, gene='dormancy')] = dataframe[t].map(lambda x: x.dormancy_time if np.all(pd.notnull(x)) else x)
# 	df['{time}_{gene}'.format(time=t, gene='offspring')] = dataframe[t].map(lambda x: x.reproduction if np.all(pd.notnull(x)) else x)
# 	df[t] = pd.Series([t] * len(dataframe[t]))
# 	# df['{time}_{gene}'.format(time=t, gene="dormancy")] = pd.cut(df['{time}_{gene}'.format(time=t, gene="dormancy")], dorm_bins, labels=dorm_bins[0:-1])
# 	# df['{time}_{gene}'.format(time=t, gene='offspring')] = pd.cut(df['{time}_{gene}'.format(time=t, gene="offspring")], rep_bins, labels=rep_bins[0:-1])
# 	for gene in ['dormancy', 'offspring']:
# 		temp = '{time}_{gene}'.format(time=t, gene=gene)
# 		data = data.append({'value': list(df[temp].values), 'key': temp}, ignore_index=True)
# print(data)

# df = df.dropna()

# figure = {
# 'data': [],
# 'layout': {},
# 'frames': [],
# }
# config = {'scrollzoom': True}


# # fill in most of layout
# figure['layout']['xaxis'] = {'range':[2.0,6.0],'title': 'Offspring', 'gridcolor': '#FFFFFF'}
# figure['layout']['yaxis'] = {'range':[500,1000], 'title': 'Dormancy', 'gridcolor': '#FFFFFF'}
# figure['layout']['hovermode'] = 'closest'
# figure['layout']['height'] = '750'
# figure['layout']['width'] = '750'
# figure['layout']['plot_bgcolor'] = 'rgb(223, 232, 243)'

# figure['layout']['sliders'] = {
# 'args': [
# 'slider.value', {
# 'duration': 30,
# 'ease': 'cubic-in-out'
# }
# ],
# 'initialValue': '100',
# 'plotlycommand': 'animate',
# 'values': time,
# 'visible': True
# }

# figure['layout']['updatemenus'] = [
# {'buttons': [
# {'args': [None, {'frame': {'duration': 100, 'redraw': True},
# 'fromcurrent': True, 'transition': {'duration': 30, 'easing': 'quadratic-in-out'}}],
# 'label': 'Play',
# 'method': 'animate'
# },
# {'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate',
# 'transition': {'duration': 0}}],
# 'label': 'Pause',
# 'method': 'animate'
# }
# ],
# 'direction': 'left',
# 'pad': {'r': 10, 't': 87},
# 'showactive': False,
# 'type': 'buttons',
# 'x': 0.1,
# 'xanchor': 'right',
# 'y': 0,
# 'yanchor': 'top'
# }
# ]

    # layout = go.Layout(
    #     xaxis=dict( ticks='', showgrid=False, zeroline=False, nticks=20 ),
    #     yaxis=dict( ticks='', showgrid=False, zeroline=False, nticks=20 ),
    #     autosize=False,
    #     height=550,
    #     width=550,
    #     hovermode='closest',

    # )

# sliders_dict = {'active': 0,'yanchor': 'top','xanchor': 'left',
# 'currentvalue': {'font': {'size': 20},'prefix': 'Time:','visible': True,'xanchor': 'right'},
# 'transition': {'duration': 30, 'easing': 'cubic-in-out'},
# 'pad': {'b': 10, 't': 50},
# 'len': 0.9,
# 'x': 0.1,
# 'y': 0,
# 'steps': []
# }
dataset = []
frames = [{'data': [{
'type':"histogram2d",
'y':list(dataframe[t].dropna().apply(lambda x: x.dormancy_time).values),
'x':list(dataframe[t].dropna().apply(lambda x: x.reproduction).values),
    # 'mode':'markers',
"colorscale":'YIGnBu',
    # "zmax":50,
"nbinsx":50,
"nbinsy":50,
    # "zauto":False,
}], 'name': t, 'traces':[0]} for t in time]
    # for gene in ['dormancy_time', 'offspring']:
    #    temp = '{time}_{gene}'.format(time=t, gene=gene)
    #    data = data.append({'value': list(dataframe[t].dropna().apply(lambda x: x.dormancy_time).values), 'key': '{time}_dormancy_time'.format(time=t)}, ignore_index=True)
    #    data = data.append({'value': list(dataframe[t].dropna().apply(lambda x: x.reproduction).values), 'key': '{time}_reproduction'.format(time=t)}, ignore_index=True)
    #    trace1 = go.Scatter(
    #     y=df.loc[data['key']=='{time}_dormancy_time'.format(time=t)].values,
    #     #list(dataframe[t].dropna().apply(lambda x: x.dormancy_time).values),
    #     x=df.loc[data['key']=='{time}_reproduction'.format(time=t)].values,
    #     #list(dataframe[t].dropna().apply(lambda x: x.reproduction).values),
    #     mode='markers',
    #     showlegend=False,
    #     marker=dict(
    #         symbol='x',
    #         opacity=0.7,
    #         color='white',
    #         size=8,
    #         line=dict(width=1),
    #     )
    # )
    # print(list(dataframe[t].dropna().apply(lambda x: x.reproduction).values))
    # data_dict = {
    # 'type':"histogram2d",
    # 'y':list(dataframe[t].dropna().apply(lambda x: x.dormancy_time).values),
    # 'x':list(dataframe[t].dropna().apply(lambda x: x.reproduction).values),
    # # 'mode':'markers',
    # "colorscale":'YIGnBu',
    # # "zmax":50,
    # "nbinsx":50,
    # "nbinsy":50,
    # # "zauto":False,
    # }

    # values = go.Histogram2d(data_dict)
        
    # )
    # layout = go.Layout(
    #     xaxis=dict( ticks='', showgrid=False, zeroline=False, nticks=20 ),
    #     yaxis=dict( ticks='', showgrid=False, zeroline=False, nticks=20 ),
    #     autosize=False,
    #     height=550,
    #     width=550,
    #     hovermode='closest',

    # )
    #values = [trace1, trace2]
    # frame['data'].append(data_dict)
dataset=frames[0]['data']
    #figure['frames'].append(frame)
    # figure['data'].append(data_dict)
    # frames.append(frame)
    # slider_step = {'args':
    # [[str(t)], {'frame': {'duration': 30, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 0}}],
    # 'label': t, 'method': 'animate'}
    # sliders_dict['steps'].append(slider_step)
    #data.append(values)

# figure['layout']['sliders'] = [sliders_dict]
fig = dict(data=dataset, layout=layout, frames=frames)

# print(figure['data'])
# fig = dict(data=figure['data'], layout=figure['layout'], frames=figure['frames'])
#fig = go.Figure(data=data, layout=layout)
py.offline.plot(fig)
# #no longer column names but instead 'value' with columns
# col_name_template = '{time}_{gene}'
# for t in time:
#     frame = {'data': [], 'name': str(t)}
#     x = (df.loc[data['key']==col_name_template.format(time=t, gene='dormancy')].values)
#     if len(x)>0:
#         data_dict = {
#         'xsrc': x[0],
#         'ysrc': df.loc[data['key']==col_name_template.format(time=t, gene='offspring')].values[0],
#         'mode': 'markers',
#             # 'textsrc': final[col_name_template.format(
#             #     year=year, continent=continent, header='country'
#             # )),
#         'marker': {'sizemode': 'area',
#         'sizeref': 200000,
#             #     'sizesrc': grid.get_column_reference(col_name_template.format(
#             #          year=year, continent=continent, header='Total_population'
#             #     )),
#         'color': (0,0,255)
#             },
#         'name': t}
#         frame['data'].append(data_dict)
#         figure['frames'].append(frame)
#         slider_step = {'args':
#         [[t], {'frame': {'duration': 100, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 100}}],
#         'label': t,
#         'method': 'animate'}
#         sliders_dict['steps'].append(slider_step)

# figure['layout']['sliders'] = [sliders_dict]
# py.offline.plot(figure, validate=False)

# # py.icreate_animations(figure)
