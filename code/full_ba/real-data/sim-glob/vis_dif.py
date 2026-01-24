import numpy as np
import pyvista as pv
import sys
from vedo import * 
from numpy import linalg as LA

vtk = sys.argv[1]

m = pv.read(vtk)
points = m.points

file = sys.argv[2]

difs = np.loadtxt(file, delimiter=',')
content = list(map(lambda x: x[0], difs))

pts = Points(points, r=6, c='green', alpha=1.0)
pts.pointdata["deformation"] = content
pts.cmap("coolwarm").add_scalarbar("deformation")

plt = Plotter()
plt.show(pts).interactive().close()
