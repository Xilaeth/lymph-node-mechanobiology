import sys
import numpy as np
from PIL import Image
from math import floor

def isInSquare(x, l, v):
    if ((abs(v[0] - x[0]) < l/2) and (abs(v[1] - x[1]) < l/2)):
        return True
    return False

file = open(sys.argv[1], "rt")
content = file.read()
lines = content.splitlines()
lines = lines[6:]

coords = []

sc = 0
for i in lines:
    if (not(i)):
        break
    if (sc == 0):
        coords.append(i)

coords = list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords))

xs = list(map(lambda x: x[0], coords))
ys = list(map(lambda x: x[1], coords))

f1 = 0.98 # float(sys.argv[3])
f = 0.95 #float(sys.argv[4])
fm = 1 - f

xop = f1*max(xs)
yop = f1*max(ys)
xom = f1*min(xs)
yom = f1*min(ys)
dx = xop - xom
dy = yop - yom
xc = xom + dx/2
yc = yom + dy/2
x = [xc, yc]
lx = f*dx
ly = f*dy
l = min(lx, ly)

mask = sys.argv[2]

x = [xc, yc]

im = Image.open("../pngs/" + mask + ".png", 'r') 
width, height = im.size
pixel_values = list(im.getdata())
pixel_values = np.array(pixel_values).reshape((width, height, 4))
coordsOut = []
typ = []

for v in coords:
    if (not(isInSquare(x, l, v))):
        continue
    px = floor((v[0] + (l/2 - x[0]))*500/l)
    py = floor((v[1] + (l/2 - x[1]))*500/l)
    if (pixel_values[px][py][0] != 0):
        coordsOut.append(v)
        typ.append(1)
    else:
        coordsOut.append(v)
        typ.append(2)


xs = list(map(lambda x: x[0], coordsOut))
ys = list(map(lambda x: x[1], coordsOut))

leng = len(xs)
out = "out_" + mask

with open(out + ".vtk", "w", encoding="ascii") as f:
    f.write("# vtk DataFile Version 3.0\n")
    f.write(out + "\n")
    f.write("ASCII\n")
    f.write("DATASET POLYDATA\n\n")
    f.write("POINTS " + str(leng) + " float\n")
    for i in coordsOut:
        f.write(str(i[0]) + " " + str(i[1]) + " " + "0.0\n")
    f.write("\nPOINT_DATA " + str(leng) + "\n")
    f.write("SCALARS v float\n")
    f.write("LOOKUP_TABLE default\n")
    for i in typ:
        f.write(str(i) + "\n")
