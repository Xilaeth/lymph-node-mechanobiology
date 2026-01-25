import sys
import numpy as np
from vedo import *
import pyvista as pv

path = sys.argv[1]
n = int(sys.argv[2])

coords_tot = []
t_tot = []

for i in range(n):
    om = pv.read(f"{path}{i}.vtk")
    coords = om.points
    t = om.point_data["t"]

    coords_tot.append(coords)
    t_tot.append(t)

xs = np.array(coords_tot)[:, :, 0].ravel()
ys = np.array(coords_tot)[:, :, 1].ravel()

maxx = max(xs)
minx = min(xs)
maxy = max(ys)
miny = min(ys)
dx = maxx - minx
dy = maxy - miny

p1 = []
p2 = []

for i in range(len(coords_tot)):
    p1_temp = []
    p2_temp = []
    for j in range(len(coords_tot[0])):
        if (t_tot[i][j] == 1):
            p1_temp.append(coords_tot[i][j])
        else:
            p2_temp.append(coords_tot[i][j])
    p1.append(p1_temp)
    p2.append(p2_temp)

plt = Plotter(offscreen=True)

pts1 = Points(p1[0], r=10, c="green", alpha=1.0)
pts2 = Points(p2[0], r=10, c="grey", alpha=1.0)
txt = Text2D(txt="T=0", pos="top left").font("Calibri")
axis = Axes(
    xtitle="x",
    ytitle="y",
    xrange=(minx - 0.05*dx, maxx + 0.05*dx),
    yrange=(miny - 0.05*dy, maxy + 0.05*dy),
)
plt.show(pts1, pts2, txt, axis)
plt.screenshot("s0.png")
pts1.points = p1[100]
pts2.points = p2[100]
txt.text(f"T=100")
plt.render()
plt.screenshot("s100.png")
plt.close()
