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
n = int(sys.argv[4])

file = sys.argv[2]

difs = np.loadtxt(file, delimiter=',')
content = list(map(lambda x: x[d], difs))

c2 = []

for i in range(len(content)):
    if (typ[i] == 1):
        c2.append(content[i])

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

ind = np.argsort(c2)[-n:]

i2 = 0
for i in range(len(typ)):
    v = points[i]
    if (((v[0] > (minx + (1-p)*dx)) and (v[0] < (minx + p*dx))) and ((v[1] > (miny + (1-p)*dy)) and (v[1] < (miny + p*dy)))):
        if (typ[i] == 1):
            if (i2 in ind):
                p2.append(points[i])
            else:
                p1.append(points[i])
                c1.append(content[i])
            i2 += 1
        else:
            p2.append(points[i])
    else:
        p2.append(points[i])

pts1 = Points(p1, r=6, c='green', alpha=1.0)
pts1.pointdata["deformation"] = c1
pts1.cmap("coolwarm").add_scalarbar("deformation")
pts2 = Points(p2, r=6, c='grey', alpha=0.2)

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
