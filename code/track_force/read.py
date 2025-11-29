import numpy as np
import sys

# read the file and split it by lines -> remove the first 6 lines
file = open(f"{sys.argv[1]}", "rt")
content = file.read()
lines = content.splitlines()
lines = lines[6:]

pos = []
force = []

sc = 0
for i in lines:
    if (not(i) or ((sc < 6 + len(pos)) and (sc > 0))):
        sc += 1
        continue
    if (sc == 0):
        pos.append(i)
    if (sc > 0):
        force.append(i)

pos = list(map(lambda x: list(map(lambda y: float(y), x.split(' ')))[:2], pos))
force = list(map(lambda x: float(x), force))

xs = list(map(lambda x: x[0], pos))
ys = list(map(lambda x: x[0], pos))

with open("positions.vtk", "w", encoding="ascii") as f:
    f.write("# vtk DataFile Version 3.0\n")
    f.write("positions" + "\n")
    f.write("ASCII\n")
    f.write("DATASET POLYDATA\n\n")
    f.write("POINTS " + str(len(pos)) + " float\n")
    for i in pos:
        f.write(str(i[0]) + " " + str(i[1]) + " " + "0.0\n")

with open("forces.csv", "w", encoding="ascii") as f:
    for i in range(len(force)):
        if (i == (len(force) - 1)):
            f.write(f"{force[i]}")
        else:
            f.write(f"{force[i]},")
