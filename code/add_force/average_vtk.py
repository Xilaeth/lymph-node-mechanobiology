import numpy as np
import matplotlib.pyplot as plt
import sys

file_t = open(f"{sys.argv[1]}-0.vtk", "rt")
content_t = file_t.read()
lines_t = content_t.splitlines()
lines_t = lines_t[6:]

coords = []

sc = 0
sc2 = 0
for i in lines_t:
    if (not(i) or ((sc < 6 + len(coords)) and (sc > 0))):
        sc += 1
        continue
    if (sc == 0):
        coords.append(i)
    if ((i[0] == "S") or ((sc2 < 2) and (sc2>0))):
        sc2 += 1
        continue
    if (sc2 > 0):
        continue
    if (sc > 0):
        continue

n = len(coords)

out = np.zeros((n, 3))

for l in range(0, int(sys.argv[2])):
    file = open(f"{sys.argv[1]}-{l}.vtk", "rt")
    content = file.read()
    lines = content.splitlines()
    lines = lines[6:]
    coords = []
    sc = 0
    sc2 = 0
    for i in lines:
        if (not(i) or ((sc < 6 + len(coords)) and (sc > 0))):
            sc += 1
            continue
        if (sc == 0):
            coords.append(i)
        if ((i[0] == "S") or ((sc2 < 2) and (sc2>0))):
            sc2 += 1
            continue
        if (sc2 > 0):
            continue
        if (sc > 0):
            continue
    coords = np.array(list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords)))
    out += coords 

out /= int(sys.argv[2])

with open(f"{sys.argv[3]}.vtk", "w", encoding="ascii") as f:
    f.write("# vtk DataFile Version 3.0\n")
    f.write(f"{sys.argv[3]}" + "\n")
    f.write("ASCII\n")
    f.write("DATASET POLYDATA\n\n")
    f.write("POINTS " + str(len(out)) + " float\n")
    for i in out:
        f.write(str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + "\n")
