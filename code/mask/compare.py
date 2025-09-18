import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from math import floor

data1 = np.loadtxt("hole_data-1.csv", delimiter=",")
data2 = np.loadtxt("hole_data-2.csv", delimiter=",")

dataDif = []

for i in range(len(data1)):
    dataDif.append([data1[i][0], data1[i][1], data2[i][2] - data1[i][2]])

# Convert to array for easier manipulation
arr = np.array(dataDif)
xs = arr[:,0].astype(int)
ys = arr[:,1].astype(int)
vals = arr[:,2]

# Determine grid size
# (max index +1 to include zero-based)
nx = xs.max() + 1
ny = ys.max() + 1

# Create an empty grid, fill with e.g. nan for missing data
grid = np.full((ny, nx), np.nan)

# Fill in values
for x, y, v in zip(xs, ys, vals):
    grid[y, x] = abs(v)

plt.imshow(grid, origin='lower', cmap='Reds', interpolation='none')
plt.show()
