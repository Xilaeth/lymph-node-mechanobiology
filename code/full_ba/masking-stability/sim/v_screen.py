import sys
import numpy as np
from vedo import *
import pyvista as pv

path = sys.argv[1]
n = int(sys.argv[2])

coords_tot = []

for i in range(n):
    om = pv.read(f"{path}{i}.vtk")
    coords = om.points

    coords_tot.append(coords)

xs = np.array(coords_tot)[:, :, 0].ravel()
ys = np.array(coords_tot)[:, :, 1].ravel()

maxx = max(xs)
minx = min(xs)
maxy = max(ys)
miny = min(ys)
dx = maxx - minx
dy = maxy - miny

plt = Plotter(offscreen=True)

pts1 = Points(coords_tot[0], r=10, c="green", alpha=1.0)
txt = Text2D(txt="T=0", pos="top left").font("Calibri")
axis = Axes(
    xtitle="x",
    ytitle="y",
    xrange=(minx - 0.05*dx, maxx + 0.05*dx),
    yrange=(miny - 0.05*dy, maxy + 0.05*dy),
)
plt.show(pts1, txt, axis)
plt.screenshot("s0.png")
pts1.points = coords_tot[100]
txt.text(f"T=100")
plt.render()
plt.screenshot("s100.png")
plt.close()
