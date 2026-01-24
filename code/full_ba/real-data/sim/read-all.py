import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv
import sys

Fs = []
FsVar = []
n = int(sys.argv[2])
path = sys.argv[1]

for l in range(n + 1):
    m = pv.read(folder + "/" + f"out-{c}_0.vtk")
    pos = m.points
    force = m.point_data["f"]

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
