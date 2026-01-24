import os
import sys
import numpy as np
import pyvista as pv

file_name = sys.argv[1]
d = int(sys.argv[2])

vtk = pv.read(file_name)
points = vtk.points

xmin = min(points[:, 0])  
xmax = max(points[:, 0])  
ymin = min(points[:, 1])  
ymax = max(points[:, 1])  
zmin = min(points[:, 2])  
zmax = max(points[:, 2])  

out = [[xmin, xmax], [ymin, ymax], [zmin, zmax]]

with open(f"out_stretch.csv", "w", encoding="ascii") as f:
    f.write(f"{out[d][0]},{out[d][1]}")
