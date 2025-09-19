import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from math import floor
import sys

data = np.loadtxt(sys.argv[1], delimiter=",")

# Convert to array for easier manipulation
arr = np.array(data)
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
    grid[y, x] = v

plt.imshow(grid, origin='lower', cmap='Greens', interpolation='none')
plt.show()
