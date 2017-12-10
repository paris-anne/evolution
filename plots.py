1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
import matplotlib.pyplot as pl
import pandas as pd 
from scipy.optimize import curve_fit
import numpy as np
from scipy.integrate import odeint
import environment as enviro
import matplotlib.animation as animation
 
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
    # state0 = [20]
    # state = odeint(LotkaVolterra, state0, t)
    # popt, pcov = curve_fit(func, list(dataframe), population.ix[0].tolist(), p0=(1, 1e-6, 1))
    # print(popt)
    # food=[0.1] * len(df.ix[:,0].values)
    ax1 = pl.subplot(211)
    ax1.title.set_text("Bacteria Population")
    print(df.ix[:,0].values)
    pl.plot(t, pop)
    #pl.plot(t, state)
    #pl.plot(list(dataframe), func(np.array(list(dataframe)), -1.71109885e-06, 4.26620601e-08, 2.00000017e+01))
    # pl.setp(ax1.get_xticklabels(), visible=False)
    # ax2 = pl.subplot(212, sharex=ax1)
    # ax2.title.set_text("Food Concentration")
    # pl.plot(df.ix[:,0].values, food)
    # pl.setp(ax2.get_xticklabels(), fontsize=6)
    pl.savefig("LV_equations.png")
    pl.show()
 
def plot_population(data):
    dataframe = dataframe.ix[:,1:-1]
    df = pd.DataFrame(t.dropna())
 
def offspring_analysis(data):
    offspring = data.iloc[:, -1].apply(lambda x: x.reproduction if (np.all(pd.notnull(x))) else x)
    foodlevel = data.iloc[:, -1].apply(lambda x: x.food_level if (np.all(pd.notnull(x))) else x)
    merge = pd.concat([offspring, foodlevel], axis=1)
    merge.to_csv("offspring_v_foodlevel.csv")
 
def antibiotic_conc_v_population(data):
    population=pd.DataFrame(data.count())
    #print(da)
    antibiotics=data.iloc[0,:].apply(lambda x: x.enviro.antibiotics_effectiveness)
    #print(antibiotics)
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
    pl.hist2d(offspring.iloc[:,0].values, dormancy.iloc[:,0].values, bins=100, cmap='Blues')
    cb = pl.colorbar()
    cb.set_label('counts in bin')
    pl.savefig("histogram.png")
    pl.show()
 
def resistance(data):
    #resistance = pd.DataFrame.sum(data.iloc[:,-1].dropna().apply(lambda x: x.resistance))
    #print(resistance, "resistance")
    print(data.iloc['resistance':,-1].dropna())
 
def population(data):
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
    pl.savefig("bacteria_population.png")
    pl.show()
def histogram(data):
    df = pd.DataFrame(data.iloc[:,-1])
    df = df.dropna()
    offspring = pd.DataFrame(data.iloc[:,-1].dropna().apply(lambda x: x.reproduction))
    dormancy = pd.DataFrame(data.iloc[:,-1].dropna().apply(lambda x: x.dormancy_time))
    print(offspring.iloc[:,0].values)
    pl.hist2d(offspring.iloc[:,0].values, dormancy.iloc[:,0].values, bins=100, cmap='Blues')
    cb = pl.colorbar()
    cb.set_label('counts in bin')
    pl.savefig("histogram.png")
    pl.show()
 
def generations_hist(data, data1, frames):
    def update_hist(num, data, data1):
        pl.clf()
        pl.hist2d(data[num][0], data1[num][0], bins=50, cmap='Blues')
        pl.title("Dormancy time and frequency distribution at time: " + str(data[num][1]))
        pl.xlabel("Dormancy time")
        pl.ylabel("Dormancy Frequency")
        cb = pl.colorbar()
        cb.set_label('counts in bin')
 
    frames1 = int(frames - frames%1)
 
    # Writer = animation.writers['imagemagick']
    # writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    #writer = animation.ImageMagickFileWriter()
 
 
    fig = pl.figure(11)
 
    ani = animation.FuncAnimation(fig, update_hist, frames1, fargs = (data, data1))
    ani.save('animation.gif', writer = "imagemagick")
    pl.show()
 
 
def dormancytime_hist(hist_data, frames):
    def update_hist(num, data):
        pl.cla()
        pl.hist(hist_data[num][0])
        pl.title("Dormancy time distribution at time: " + str(hist_data[num][1] ))
        pl.xlabel("Dormancy time")
        pl.ylabel("Frequency")
    frames1 = int(frames - frames%1)
 
    # Writer = animation.writers['imagemagick']
    # writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    #writer = animation.ImageMagickFileWriter()
 
 
    fig = pl.figure(11)
    ani = animation.FuncAnimation(fig, update_hist, frames1, fargs = (hist_data,))
    ani.save('blaisematuidi.gif', writer = "imagemagick", fps=60)
    print(animation.writers.list())
 
    pl.show()
 
def dormancyfreq_hist(hist_data, frames):
    def update_hist(num, data):
        pl.cla()
        pl.hist(hist_data[num][0])
        pl.title("Dormancy freq distribution at time: " + str(hist_data[num][1] ))
        pl.xlabel("Dormancy freq")
        pl.ylabel("Frequency")
    frames1 = int(frames - frames%1)
 
    # Writer = animation.writers['imagemagick']
    # writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    #writer = animation.ImageMagickFileWriter()
 
 
    fig = pl.figure(12)
    ani = animation.FuncAnimation(fig, update_hist, frames1, fargs = (hist_data,))
    ani.save('animation.gif', writer = "imagemagick")
    pl.show()
 
def dormancyfreqplustime_hist(hist_data, frames):
    def update_hist(num, data):
        pl.cla()
        pl.hist(hist_data[num][0])
        pl.title("Dormancy freq + time distribution at time: " + str(hist_data[num][1] ))
        pl.xlabel("Dormancy freq + time")
        pl.ylabel("Frequency")
    frames1 = int(frames - frames%1)
 
    # Writer = animation.writers['imagemagick_file']
    # writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    #writer = animation.ImageMagickFileWriter()
     
    # FFMpegWriter = manimation.writers['ffmpeg']
    # metadata = dict(title='Movie Test', artist='Matplotlib',
 #                comment='Movie support!')
    # writer = FFMpegWriter(fps=15, metadata=metadata)
 
 
 
    fig = pl.figure(13)
    ani = animation.FuncAnimation(fig, update_hist, frames1, fargs = (hist_data,))
    ani.save('animation.gif', writer = "imagemagick_file")
    pl.show()
 
 
 
#def changing_conc