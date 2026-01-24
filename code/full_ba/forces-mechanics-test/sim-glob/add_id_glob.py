import os
import sys
import numpy as np
import pyvista as pv

file_name = sys.argv[1]
out = sys.argv[2]
p = float(sys.argv[3])

vtk = pv.read(file_name)
coords = vtk.points

xs = np.array(coords)[:, 0].ravel()
ys = np.array(coords)[:, 1].ravel()

maxx = max(xs)
minx = min(xs)
maxy = max(ys)
miny = min(ys)
dx = maxx - minx
dy = maxy - miny

leng = len(coords)

ids = []

for v in coords:
    if (v[0] > (minx + (1-p)*dx)):
        if (v[1] > (miny + (1-p)*dy)):
            ids.append(2)
        elif (v[1] < (miny + p*dy)):
            ids.append(8)
        else:
            ids.append(1)
        
    elif (v[0] < (minx + p*dx)):
        if (v[1] > (miny + (1-p)*dy)):
            ids.append(4)
        elif (v[1] < (miny + p*dy)):
            ids.append(6)
        else:
            ids.append(5)
    else:
        if (v[1] > (miny + (1-p)*dy)):
            ids.append(3)
        elif (v[1] < (miny + p*dy)):
            ids.append(7)
        else:
            ids.append(0)


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
    for i in range(leng):
        f.write(str(ids[i]) + "\n")
