import os
import sys
import numpy as np
import pyvista as pv

file_name = sys.argv[1]
out = sys.argv[2]

vtk = pv.read(file_name)
coords = vtk.points
typ = vtk.point_data["t"]

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
    f.write("SCALARS t float\n")
    f.write("LOOKUP_TABLE default\n")
    for i in range(leng):
        f.write(f"{typ[i]}\n")
    f.write("SCALARS v float\n")
    f.write("LOOKUP_TABLE default\n")
    for i in range(leng):
        f.write(str(i) + "\n")
