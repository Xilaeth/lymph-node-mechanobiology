import os
import sys
import numpy as np

file = open(sys.argv[1], "rt")
content = file.read()
lines = content.splitlines()
lines = lines[6:]

coords = []
fo = []

sc = 0
for i in lines:
    if (not(i) or (sc>0 and sc<4)):
        sc += 1
    elif ((sc > 0) and (not(i))):
        break
    elif (sc == 0):
        coords.append(i)
    elif (sc > 0):
        fo.append(i)   

coords = list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords))
fo = list(map(lambda x: int(x), fo))

xmin = min(np.array(coords)[:, 0])
xmax = max(np.array(coords)[:, 0])
ymin = min(np.array(coords)[:, 1])
ymax = max(np.array(coords)[:, 1])
lx = xmax - xmin
ly = ymax - ymin

out = sys.argv[2]
leng = len(coords)
fxs = float(sys.argv[3])
fxe = float(sys.argv[4])
fys = float(sys.argv[5])
fye = float(sys.argv[6])
x = 0.5*( (xmin + fxs*lx) + (xmin + fxe*lx) )
y = 0.5*( (ymin + fys*ly) + (ymin + fye*ly) )
dx = lx*(fxe - fxs)
dy = ly*(fye - fys)


def isIn(v):
    if ((np.abs(v[0] - x) <= dx/2) and (np.abs(v[1] - y) <= dy/2)):
        return True
    else:
        return False

with open(f"{out}.vtk", "w", encoding="ascii") as f:
    f.write("# vtk DataFile Version 3.0\n")
    f.write(out + "\n")
    f.write("ASCII\n")
    f.write("DATASET POLYDATA\n\n")
    f.write("POINTS " + str(leng) + " float\n")
    for i in coords:
        f.write(str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + "\n")
    f.write("\nPOINT_DATA " + str(leng) + "\n")
    f.write("SCALARS ct float\n")
    f.write("LOOKUP_TABLE default\n")
    for i in fo:
        f.write(str(i) + "\n")
    f.write("\nPOINT_DATA " + str(leng) + "\n")
    f.write("SCALARS fo float\n")
    f.write("LOOKUP_TABLE default\n")
    for i in range(leng):
        if (isIn(coords[i])):
            f.write("1\n")
        else:
            f.write("0\n")
