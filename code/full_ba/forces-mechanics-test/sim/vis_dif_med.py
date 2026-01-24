import numpy as np
import pyvista as pv
import sys
from vedo import * 
from numpy import linalg as LA

vtk = sys.argv[1]
n = int(sys.argv[3])

m = pv.read(vtk)
points = m.points

file = sys.argv[2]

difs = np.loadtxt(file, delimiter=',')
content = list(map(lambda x: x[0], difs))

pts1 = []
pts2 = []
c1 = []

ind = np.argsort(content)[-n:]

for i in range(len(points)):
    v = points[i]
    if (i in ind):
        pts2.append(v)
    else:
        pts1.append(v)
        c1.append(content[i])


pts = Points(pts1, r=6, c='green', alpha=1.0)
pts.pointdata["deformation"] = c1
pts.cmap("coolwarm").add_scalarbar("deformation")

pts_e = Points(pts2, r=6, c='gray', alpha=0.8)

plt = Plotter()
plt.show(pts, pts_e).interactive().close()
