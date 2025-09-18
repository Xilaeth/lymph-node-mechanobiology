import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from math import floor

file1 = open("vtks/n10000T2000dt1.vtk", "rt")
file2 = open("vtks/n10000T2000dt1.vtk", "rt")
content1 = file1.read()
content2 = file2.read()

lines1 = content1.splitlines()
lines2 = content2.splitlines()
lines1 = lines[6:]
lines2 = lines[6:]

coords1 = list(map(lambda x: list(map(lambda y: float(y), x.split(' ')))[:2], lines1))
coords2 = list(map(lambda x: list(map(lambda y: float(y), x.split(' ')))[:2], lines2))

xs1 = list(map(lambda x: x[0], coords1))
ys1 = list(map(lambda x: x[1], coords1))
xs2 = list(map(lambda x: x[0], coords2))
ys2 = list(map(lambda x: x[1], coords2))


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

inp = 'hole'

im = Image.open(inp + ".png", 'r')
width, height = im.size
pixel_values = list(im.getdata())

#print(pixel_values)

pixel_values = np.array(pixel_values).reshape((width, height, 4))

coordsOut = []

l = 36
x = [0, 0]

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

plt.scatter(xs, ys, s=1.5, c='red')
plt.axis('square')
plt.show()

