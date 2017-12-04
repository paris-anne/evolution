from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = pd.DataFrame.from_csv("population.csv")
df = pd.DataFrame(data.iloc[:,-1])
df = df.dropna()
offspring = pd.DataFrame(data.iloc[:,-1].dropna().apply(lambda x: x.reproduction))
dormancy = pd.DataFrame(data.iloc[:,-1].dropna().apply(lambda x: x.dormancy_time))
print(offspring.iloc[:,0].values)
cb = pl.colorbar()
cb.set_label('counts in bin')
pl.savefig("histogram.png")
pl.show()

for i in range(len(df.columns())):
    pl.hist2d(offspring.iloc[:,i].values, dormancy.iloc[:,i].values, bins=50, cmap='Blues')
    cb = pl.colorbar()
    cb.set_label('counts in bin')

class IndexTracker(object):
    def __init__(self, ax, X):
        self.ax = ax
        ax.set_title('use scroll wheel to navigate images')

        self.X = X
        rows, cols, self.slices = X.shape
        self.ind = self.slices//2

        self.im = ax.imshow(self.X[:, :, self.ind])
        self.update()

    def onscroll(self, event):
        print("%s %s" % (event.button, event.step))
        if event.button == 'left':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        self.update()

    def update(self):
        self.im.set_data(self.X[:, :, self.ind])
        ax.set_ylabel('time %s' % self.slices)
        self.im.axes.figure.canvas.draw()


fig, ax = plt.subplots(1, 1)

X = np.random.rand(50, 50, len(df.columns()))

tracker = IndexTracker(ax, X)


fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
plt.show()