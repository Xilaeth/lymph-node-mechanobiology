import numpy as np
import pyvista as pv
import sys
from vedo import * 
from numpy import linalg as LA

vtk = sys.argv[1]

m = pv.read(vtk)
points = m.points
typ = m.point_data["t"]
d = int(sys.argv[3]) - 1

file = sys.argv[2]

difs = np.loadtxt(file, delimiter=',')
content = list(map(lambda x: x[d], difs))

xs = np.array(points)[:, 0].ravel()
ys = np.array(points)[:, 1].ravel()

maxx = max(xs)
minx = min(xs)
maxy = max(ys)
miny = min(ys)
dx = maxx - minx
dy = maxy - miny

p1 = []
p2 = []
c1 = []

p = 0.95

#for i in range(len(typ)):
#    if (typ[i] == 1):
#        p1.append(points[i])
#        c1.append(content[i])
#    else:
#        p2.append(points[i])

for i in range(len(typ)):
    v = points[i]
    if (((v[0] > (minx + (1-p)*dx)) and (v[0] < (minx + p*dx))) and ((v[1] > (miny + (1-p)*dy)) and (v[1] < (miny + p*dy)))):
        if (typ[i] == 1):
            p1.append(points[i])
            c1.append(content[i])
        else:
            p2.append(points[i])
    else:
        p2.append(points[i])

pts1 = Points(p1, r=6, c='green', alpha=1.0)
pts1.pointdata["deformation"] = c1
pts1.cmap("coolwarm").add_scalarbar("deformation")
pts2 = Points(p2, r=6, c='grey', alpha=0.5)

axis = Axes(
    xtitle="x",
    ytitle="y",
    xrange=(minx - 0.05*dx, maxx + 0.05*dx),
    yrange=(miny - 0.05*dy, maxy + 0.05*dy),
)

plt = Plotter(offscreen=True)
plt.show(pts1, pts2, axis)
plt.screenshot("difs.png")
plt.close()
