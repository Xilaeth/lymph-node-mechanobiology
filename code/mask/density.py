import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from math import floor

file = open("vtks/hole_out.vtk", "rt")
content = file.read()
lines = content.splitlines()
lines = lines[6:]

coords = list(map(lambda x: list(map(lambda y: float(y), x.split(' ')))[:2], lines))

xs = list(map(lambda x: x[0], coords))
ys = list(map(lambda x: x[1], coords))


def isInSquare(x, l, v):
    if ((abs(v[0] - x[0]) < l/2) and (abs(v[1] - x[1]) < l/2)):
        return True
    return False

def isInCirc(x, r, v):
    if (((v[0] - x[0])**2 + (v[1] - x[1])**2) < r):
        return True
    return False

def densityInSquare(x, l):
    counter = 0
    for i in range(len(xs)):
        if (isInSquare(x, l, coords[i])):
            counter += 1
    return (counter / (l*l))

def densityInCirc(x, r):
    counter = 0
    for i in coords:
        if (isInCirc(x, r, i)):
            counter += 1
    return (counter / (np.pi * r * r))


coordsOut = []

l = 36
x = [0, 0]

n = 100
r = 0.5
vals = np.linspace(-l/2, l/2, n)

for x in range(101):
    for y in range(101):
        coordsOut.append([x, y, densityInCirc([-l/2 + x*(l/100), -l/2 + y*(l/100)], r)])

# Convert to array for easier manipulation
arr = np.array(coordsOut)
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

plt.imshow(grid, origin='lower', cmap='viridis', interpolation='none')
plt.show()
