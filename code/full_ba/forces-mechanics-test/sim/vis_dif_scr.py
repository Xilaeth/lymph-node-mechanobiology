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

xs = np.array(points)[:, 0].ravel()
ys = np.array(points)[:, 1].ravel()

maxx = max(xs)
minx = min(xs)
maxy = max(ys)
miny = min(ys)
dx = maxx - minx
dy = maxy - miny

pts = Points(points, r=6, c='green', alpha=1.0)
pts.pointdata["deformation"] = content
pts.cmap("coolwarm").add_scalarbar("deformation")
axis = Axes(
    xtitle="x",
    ytitle="y",
    xrange=(minx - 0.05*dx, maxx + 0.05*dx),
    yrange=(miny - 0.05*dy, maxy + 0.05*dy),
)
plt = Plotter(offscreen=True)
plt.show(pts, axis)
plt.screenshot("difs.png")
plt.close()
