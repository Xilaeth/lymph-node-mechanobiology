import sys
import numpy as np
import pyvista as pv
from vedo import *

file_name = "load.vtk"

for inp in sys.argv:
    if (inp[0] == "-"):
        print(":)")
    else:
        file_name = inp

m = pv.read(file_name)
coords = m.points

pts = Points(coords, r=8, c="green", alpha=1.0)

plt = Plotter()
plt.at(0).show(pts, axes=1)
plt.interactive().close()
