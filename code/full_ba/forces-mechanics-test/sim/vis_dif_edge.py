import numpy as np
import pyvista as pv
import sys
from vedo import * 
from numpy import linalg as LA

vtk = sys.argv[1]
p = float(sys.argv[3])

m = pv.read(vtk)
points = m.points

file = sys.argv[2]

difs = np.loadtxt(file, delimiter=',')
content = list(map(lambda x: x[0], difs))

xs = np.array(points)[:, 0].ravel()
ys = np.array(points)[:, 1].ravel()

maxx = max(xs)
minx = min(xs)
maxy = max(ys)
miny = min(ys)
dx = maxx - minx
dy = maxy - miny

pts1 = []
pts2 = []
c1 = []

for i in range(len(points)):
    v = points[i]
    if (((v[0] > (minx + (1-p)*dx)) and (v[0] < (minx + p*dx))) and ((v[1] > (miny + (1-p)*dy)) and (v[1] < (miny + p*dy)))):
        pts1.append(v)
        c1.append(content[i])
    else:
        pts2.append(v)


pts = Points(pts1, r=6, c='green', alpha=1.0)
pts.pointdata["deformation"] = c1
pts.cmap("coolwarm").add_scalarbar("deformation")

pts_e = Points(pts2, r=6, c='gray', alpha=0.8)

plt = Plotter()
plt.show(pts, pts_e).interactive().close()
