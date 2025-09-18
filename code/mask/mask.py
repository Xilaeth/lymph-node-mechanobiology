import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from math import floor

file = open("vtks/inp.vtk", "rt")
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

def densityInSquare(x, l):
    counter = 0
    for i in range(len(xs)):
        if (isInSquare(x, l, coords[i])):
            counter += 1
    return (counter / (l*l))

#print(densityInSquare([0, 0], 10))

inp = 'lines'

im = Image.open(inp + ".png", 'r')
width, height = im.size
pixel_values = list(im.getdata())

#print(pixel_values)

pixel_values = np.array(pixel_values).reshape((width, height, 4))

coordsOut = []

l = 15
x = [10, 7]

for v in coords:
    if (not(isInSquare(x, l, v))):
        coordsOut.append(v)
        continue
    px = floor((v[0] + (l/2 - x[0]))*500/l)
    py = floor((v[1] + (l/2 - x[1]))*500/l)
    if (pixel_values[px][py][0] == 0):
        coordsOut.append(v)


xs = list(map(lambda x: x[0], coordsOut))
ys = list(map(lambda x: x[1], coordsOut))

leng = len(xs)

out = inp + "_out"

with open(out + ".vtk", "w", encoding="ascii") as f:
    f.write("# vtk DataFile Version 3.0\n")
    f.write(out + "\n")
    f.write("ASCII\n")
    f.write("DATASET POLYDATA\n\n")
    f.write("POINTS " + str(leng) + " float\n")
    for i in coordsOut:
        f.write(str(i[0]) + " " + str(i[1]) + " " + "0.0\n")

fig, ax = plt.subplots()

# Remove axes completely
ax.set_axis_off()
#ax.set_box_aspect(1)

# Adjust figure so no padding remains
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
#ax.scatter(xs, ys, s=1.5, c='red')


#plt.show()
