import sys
import numpy as np
from math import floor
from tifffile import imread

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
zs = list(map(lambda x: x[2], coords))

f1 = 1.0
f = 1.0

xop = f1 * max(xs)
yop = f1 * max(ys)
zop = f1 * max(zs)
xom = f1 * min(xs)
yom = f1 * min(ys)
zom = f1 * min(zs)
dx = xop - xom
dy = yop - yom
dz = zop - zom
xc = xom + dx/2
yc = yom + dy/2
zc = zom + dz/2
x = [xc, yc, zc]
lx = f*dx
ly = f*dy
lz = f*dz

mask = sys.argv[2]
out = sys.argv[3]

im_data = imread(mask)
d, h, w = im_data.shape
coordsOut = []

if ((lx <= ly) and (lx*(h/w) > ly)):
    lx = ly * (w/h)
    lz = ly * (d/h)
elif ((lx <= ly) and (lx*(h/w) <= ly)):
    ly = lx *(h/w)
    lz = lx *(d/w)
elif ((ly < lx) and (ly*(w/h) > lx)):
    ly = lx * (h/w)
    lz = lx * (d/w)
elif ((ly < lx) and (ly*(w/h) <= lx)):
    lx = ly * (w/h)
    lz = ly * (d/h)

def isInRect(x, lx, ly, lz, v):
    if ((abs(v[0] - x[0]) < lx/2) and (abs(v[1] - x[1]) < ly/2) and (abs(v[2] - x[2]) < lz/2)):
        return True
    return False

for v in coords:
    if (not(isInRect(x, lx, ly, lz, v))):
        continue
    px = floor((v[0] - x[0] + lx/2)*w/lx) - 1
    py = floor((v[1] - x[1] + ly/2)*h/ly) + 1
    pz = floor((v[2] - x[2] + lz/2)*d/lz) - 1
    if (im_data[pz, h - py, px] != 0):
        coordsOut.append(v)

leng = len(coordsOut)

with open(out + ".vtk", "w", encoding="ascii") as f:
    f.write("# vtk DataFile Version 3.0\n")
    f.write(out + "\n")
    f.write("ASCII\n")
    f.write("DATASET POLYDATA\n\n")
    f.write("POINTS " + str(leng) + " float\n")
    for i in coordsOut:
        f.write(str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + "\n")
