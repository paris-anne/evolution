import numpy as np

nodormant = [16250, 16250,16250,16250]
dormancy_period1=[3750,750,3750,5250]
dormancy_period2=[1075, 6750, 12750, 12750]
offspring_dormancy1=[10600,17800,35700,16600]
offspring_dormancy2=[16800, 35600,16600,33400]
freq1 = [22600, 21600, 35700, 16800]
period1=[1500, 1500, 900, 4500]
freq2 = [20600, 10600, 28600, 33000]
period2 = [900, 3300, 5700, 3900]

items = [nodormant, dormancy_period1, dormancy_period2, offspring_dormancy1, offspring_dormancy2, freq1, period1, freq2, period2 ]

print(np.mean(dormancy_period2))
print(np.std(dormancy_period2))

