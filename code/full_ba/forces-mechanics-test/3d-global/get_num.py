import os
import sys
import numpy as np
import pyvista as pv

file_name = sys.argv[1]

vtk = pv.read(file_name)
coords = vtk.points

print(len(coords))
