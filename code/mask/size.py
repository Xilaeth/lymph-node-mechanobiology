import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from math import floor

# read the file and split it by lines -> remove the first 6 lines
file = open("vtks/load_1000.vtk", "rt")
content = file.read()
lines = content.splitlines()
lines = lines[6:]

# we create a list of the type [[x1, y1], [x2, y2],...]
coords = list(map(lambda x: list(map(lambda y: float(y), x.split(' ')))[:2], lines))

# isolate the x and y coordinates for ease of use
xs = list(map(lambda x: x[0], coords))
ys = list(map(lambda x: x[1], coords))

# function to check if a given coordinate v is in a square of side length l centered at x
def isInCirc(x, r, v):
    if ((v[0] - x[0])**2 + (v[1] - x[1])**2 < r**2):
        return True
    return False

# function that calculates the density of cells in a square of side length l centered at x
def densityInCirc(x, r):
    counter = 0
    for i in range(len(xs)):
        if (isInCirc(x, r, coords[i])):
            counter += 1
    return (counter / (np.pi*r*r))

xop, xom = 0, 0
xpend = False
xmend = False
yop, yom = 0, 0
ypend = False
ymend = False
r = 0.5

while (not(xpend) or not(ypend) or not(xmend) or not(ymend)):
    if (densityInCirc([xop, 0], r) < 1e-5):
        xpend = True
    if (densityInCirc([0, yop], r) < 1e-5):
        ypend = True
    if (densityInCirc([xom, 0], r) < 1e-5):
        xmend = True
    if (densityInCirc([0, yom], r) < 1e-5):
        ymend = True
    if (not(xpend)):
        xop += 1
    if (not(ypend)):
        yop += 1
    if (not(xmend)):
        xom -= 1
    if (not(ymend)):
        yom -= 1

xop -= r
yop -= r
xom += r
yom += r

print("x: [", xom, ", ", xop, "]")
print("y: [", yom, ", ", yop, "]")
