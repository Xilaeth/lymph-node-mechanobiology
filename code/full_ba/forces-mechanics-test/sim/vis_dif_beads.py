import numpy as np
import pyvista as pv
import sys
from vedo import * 
from numpy import linalg as LA

vtk = sys.argv[1]

m = pv.read(vtk)
points = m.points
typ = m.point_data["t"]

file = sys.argv[2]
d = int(sys.argv[3])-1

difs = np.loadtxt(file, delimiter=',')
content = list(map(lambda x: x[d], difs))

p1 = []
p2 = []
c1 = []

for i in range(len(typ)):
    if (typ[i] == 1):
        p1.append(points[i])
        c1.append(content[i])
    else:
        p2.append(points[i])

pts1 = Points(p1, r=6, c='green', alpha=1.0)
pts1.pointdata["deformation"] = c1
pts1.cmap("coolwarm").add_scalarbar("deformation")
pts2 = Points(p2, r=6, c='grey', alpha=0.5)

plt = Plotter()
plt.show(pts1, pts2).interactive().close()
