import os
import sys
import numpy as np

file_name = sys.argv[1]
out = sys.argv[2]

file = open(file_name)
content = file.read()
lines = content.splitlines()
lines = lines[6:]

coords = []
typ = []

sc = 0
sc2 = 0
for i in lines:
    if (not(i) or ((sc < 4) and (sc > 0))):
        sc += 1
        continue
    if (sc == 0):
        coords.append(i)

coords = list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords))

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
    for i in range(leng):
        f.write(str(i) + "\n")
