import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv
import sys

Fs = []
FsVar = []
n = int(sys.argv[2])
path = sys.argv[1]

for l in range(n + 1):
    om = pv.read(f"{path}{l}.vtk")
    pos = om.points
    fx = om.point_data["fx"]
    fy = om.point_data["fy"]

    with open(f"{sys.argv[3]}/positions{l}.vtk", "w", encoding="ascii") as f:
        f.write("# vtk DataFile Version 3.0\n")
        f.write("positions" + "\n")
        f.write("ASCII\n")
        f.write("DATASET POLYDATA\n\n")
        f.write("POINTS " + str(len(pos)) + " float\n")
        for i in pos:
            f.write(str(i[0]) + " " + str(i[1]) + " " + "0.0\n")

    with open(f"{sys.argv[3]}/forces{l}.csv", "w", encoding="ascii") as f:
        for i in range(len(fx)):
            if (i == (len(fx) - 1)):
                f.write(f"{fx[i]},{fy[i]}")
            else:
                f.write(f"{fx[i]},{fy[i]},")
