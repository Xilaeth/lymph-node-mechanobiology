import numpy as np
import matplotlib.pyplot as plt
import sys

file = open(f"out/out_0.vtk")
content = file.read()
lines = content.splitlines()
lines = lines[6:]

coords = []
typ = []
typ_vf = []

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
        typ.append(i)
    if (sc > 0):
        typ_vf.append(i)

n = len(coords)
out = np.zeros((n, 3))

for l in range(int(sys.argv[1])):
    file = open(f"./out/out_{l}.vtk", "rt")
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

    coords = list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords))

    out += coords 

out /= int(sys.argv[1])

leng = len(out)

with open(f"./out/average.vtk", "w", encoding="ascii") as f:
    f.write("# vtk DataFile Version 3.0\n")
    f.write("average" + "\n")
    f.write("ASCII\n")
    f.write("DATASET POLYDATA\n\n")
    f.write("POINTS " + str(len(out)) + " float\n")
    for i in out:
        f.write(str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + "\n")
    f.write("\nPOINT_DATA " + str(leng) + "\n")
    f.write("SCALARS vf float\n")
    f.write("LOOKUP_TABLE default\n")
    for i in typ_vf:
        f.write(str(i) + "\n")
    f.write("SCALARS v float\n")
    f.write("LOOKUP_TABLE default\n")
    for i in typ:
        f.write(str(i) + "\n")
