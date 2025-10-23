import os
import sys
import numpy as np

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

coords = np.array(list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords)))

xs = coords[:, 0]
ys = coords[:, 1]

mode = int(sys.argv[3])

maxy = max(ys)
miny = min(ys)
ly = maxy - miny
f = 0.9

typ = []

for i in range(len(coords)):
    if (ys[i] > (miny+f*maxy)):
        typ.append(mode)
    elif (ys[i] < (miny + (1-f)*maxy)):
        typ.append(-1)
    else:
        typ.append(0)

out = sys.argv[2]
leng = len(coords)

with open(f"{out}.vtk", "w", encoding="ascii") as f:
    f.write("# vtk DataFile Version 3.0\n")
    f.write(out + "\n")
    f.write("ASCII\n")
    f.write("DATASET POLYDATA\n\n")
    f.write("POINTS " + str(leng) + " float\n")
    for i in coords:
        f.write(str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + "\n")
    f.write("\nPOINT_DATA " + str(leng) + "\n")
    f.write("SCALARS v float\n")
    f.write("LOOKUP_TABLE default\n")
    for i in typ:
        f.write(str(i) + "\n")
