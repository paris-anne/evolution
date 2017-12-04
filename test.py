import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

df = pd.DataFrame.from_csv("population.csv")
df = df.iloc[:,-1]
df = df.dropna()

offspring = pd.DataFrame(data.apply(lambda x: x.reproduction))
dormancy = pd.DataFrame(data.apply(lambda x: x.dormancy_time))
print(offspring.iloc[:,0].values)
for i in range(len(off))
pl.hist2d(offspring.iloc[:,0].values, dormancy.iloc[:,0].values, bins=50, cmap='Blues')
cb = pl.colorbar()
cb.set_label('counts in bin')
pl.savefig("histogram.png")
pl.show()
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro', animated=True)

def init():
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)
    return ln,

def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)
    return ln,

ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                    init_func=init, blit=True)
plt.show()