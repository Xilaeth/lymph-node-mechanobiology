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
    elif (sc == 0):
        coords.append(i)
    elif (sc > 0):
        fo.append(i)   

coords = list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords))
fo = list(map(lambda x: int(x), fo))

typ = []

for i in range(len(coords)):
    typ.append(i)

out = sys.argv[2]
leng = len(coords)

c = 0

with open(f"{out}.vtk", "w", encoding="ascii") as f:
    f.write("# vtk DataFile Version 3.0\n")
    f.write(out + "\n")
    f.write("ASCII\n")
    f.write("DATASET POLYDATA\n\n")
    f.write("POINTS " + str(leng) + " float\n")
    for i in coords:
        f.write(str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + "\n")
    f.write("\nPOINT_DATA " + str(leng) + "\n")
    f.write("SCALARS f float\n")
    f.write("LOOKUP_TABLE default\n")
    for i in fo:
        f.write(str(i) + "\n")
    f.write("\nPOINT_DATA " + str(leng) + "\n")
    f.write("SCALARS v float\n")
    f.write("LOOKUP_TABLE default\n")
    for i in range(leng):
        if (fo[i] == 1):
            f.write(str(c) + "\n")
            c += 1
        elif (fo[i] == 2):
            f.write("-1\n")
