import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from math import floor
import sys

data1 = np.loadtxt(sys.argv[1], delimiter=",")
data2 = np.loadtxt(sys.argv[2], delimiter=",")

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

great = vals.copy()
great.sort()
great = list(map(lambda x: abs(x), great))
great = great[-(int(len(vals)/10)):]

# take the greatest 10% of change as a cut-off filter
for x, y, v in zip(xs, ys, vals):
    grid[y, x] = abs(v)

fig, ax = plt.subplots()
ax.imshow(grid, origin='lower', cmap='Reds', interpolation='none')

# Remove axes completely
ax.set_axis_off()

# Adjust figure so no padding remains
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

# Save with the same resolution as the figure (default DPI * figure size)
#fig.savefig("plot.png", dpi=fig.dpi, bbox_inches='tight', pad_inches=0, transparent=True)

plt.show()
