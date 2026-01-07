import numpy as np
import matplotlib.pyplot as plt
import sys

Fs = []
FsVar = []
n = int(sys.argv[2])
path = sys.argv[1]

for l in range(n + 1):
    file = open(f"{sys.argv[1]}{l}.vtk", "rt")
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
        if ((sc >= 6 + len(pos)) and i[0] == 'S'):
            break
        if (sc == 0):
            pos.append(i)
        if (sc > 0):
            force.append(i)

    pos = list(map(lambda x: list(map(lambda y: float(y), x.split(' ')))[:2], pos))
    force = list(map(lambda x: np.abs(float(x)), force))
    for i in range(len(force)):
        if (np.abs(force[i]) > 1):
            force[i] = 0

    xs = list(map(lambda x: x[0], pos))
    ys = list(map(lambda x: x[0], pos))

    with open(f"{sys.argv[3]}/positions{l}.vtk", "w", encoding="ascii") as f:
        f.write("# vtk DataFile Version 3.0\n")
        f.write("positions" + "\n")
        f.write("ASCII\n")
        f.write("DATASET POLYDATA\n\n")
        f.write("POINTS " + str(len(pos)) + " float\n")
        for i in pos:
            f.write(str(i[0]) + " " + str(i[1]) + " " + "0.0\n")

    with open(f"{sys.argv[3]}/forces{l}.csv", "w", encoding="ascii") as f:
        for i in range(len(force)):
            if (i == (len(force) - 1)):
                f.write(f"{force[i]}")
            else:
                f.write(f"{force[i]},")
