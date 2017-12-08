import pandas as pd
import numpy as np
import plotly as py
from plotly.tools import FigureFactory as ff 
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot

from plotly.grid_objs import Grid, Column
import plotly.graph_objs as go

dataframes = []

dataframe = pd.read_pickle("total.pkl").iloc[:,:-1]
#dataframe = pd.concat([dataframe1, dataframe2])
time = list(dataframe.columns)

def get_sliders(n_frames, fr_duration=100, x_pos=0.0, slider_len=1.0):
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

def get_updatemenus(x_pos=0.0, fr_duration=100):
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

def histo_offspring(dataframe):
    time = list(dataframe.columns)
    layout=dict(width=750, height=750,
            # font=dict(family='Balto', 
            #           size=12),

            xaxis= dict(range= [1.5,17.5], 
                        title="Number of Offspring"),
                        # ticklen=4,  
                        # autorange= False, 
                        # zeroline=False, 
                        # showline=True, 
                        # mirror=True,
                        # showgrid=True),
            yaxis=dict(range= [1000, 10000], 
                        title= "Dormancy Time"),
                       # ticklen=4,  
                       # autorange= False, 
                       # showline=True, 
                       # mirror=True,
                       # zeroline=False, 
                       # showgrid=True),
            # plot_bgcolor = 'rgb(223, 232, 243)',
            title= 'Evolution', 
            hovermode='closest',
            gridcolour='#FFFFFF',
            sliders=get_sliders(n_frames=len(time)),
            updatemenus=get_updatemenus()
            )
    frames = [{'data': [{
    'type':"histogram2d",
    'y':list(dataframe[t].dropna().apply(lambda x: x.dormancy_time).values),
    'x':list(dataframe[t].dropna().apply(lambda x: x.reproduction).values),
    'autobinx':False,
    'xbins':dict(start=1.5, end=17.5, size=2),
    'autobiny':False,
    'ybins':dict(start=0000, end=5000, size=300),
    "colorscale":'YIGnBu',
    #     # "zmax":50,
    "nbinsx":50,
    "nbinsy":5,
        # "zauto":False,
    }], 'name': t} for t in time]
#, 'traces':[0]

    dataset=frames[0]['data']
    print(dataset)

    fig = dict(data=dataset, layout=layout, frames=frames)

    py.offline.plot(fig)
    return fig

def histo_dormancy(dataframe):
    time = list(dataframe.columns)
    layout=dict(width=750, height=750,
            # font=dict(family='Balto', 
            #           size=12),
            xaxis= dict(range= [1000,5000], 
                        ticklen=4,  
                        autorange= False, 
                        zeroline=False, 
                        showline=True, 
                        mirror=True,
                        showgrid=True),
            yaxis=dict(range= [1000, 10000], 
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
            updatemenus=get_updatemenus(),
            )
    frames = [{'data': [{
    'type':"histogram2d",
    'y':list(dataframe[t].dropna().apply(lambda x: x.dormancy_time).values),
    'x':list(dataframe[t].dropna().apply(lambda x: x.dormancy_period).values),
    'autobinx':False,
    'xbins':dict(start=1000, end=40000, size=300),
    'autobiny':False,
    'ybins':dict(start=0, end=5000, size=50),
        
    "colorscale":'YIGnBu',
    #     # "zmax":50,
    # "nbinsx":1,
    # "nbinsy":50,
        # "zauto":False,
    }], 'name': t, 'traces':[0]} for t in time]


    dataset=frames[0]['data']
    print(dataset)

    fig = dict(data=dataset, layout=layout, frames=frames)

    py.offline.plot(fig)
    return fig

dormancy_offspring = histo_offspring(dataframe)
#dormancy = histo_dormancy(dataframe) #change dimensions
