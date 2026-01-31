import sys
import numpy as np
from vedo import *

path = sys.argv[1]
n = int(sys.argv[2])

coords_tot = []
typ_tot = []

for i in range(n):
    file = open(f"{path}{i}.vtk")
    content = file.read()
    lines = content.splitlines()
    lines = lines[6:]

    coords = []
    typ = []

    sc = 0
    sc2 = 0
    for i in lines:
        if (not(i) or ((sc < 6 + len(coords)) and (sc > 0))):
            sc += 1
            continue
        if (sc == 0):
            coords.append(i)
        if ((i[0] == "S") or ((sc2 < 2) and (sc2>0))):
            sc2 += 1
            continue
        if (sc2 > 0):
            typ.append(i)
        if (sc > 0):
            continue


    coords = list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords))
    typ = list(map(lambda x: int(x), typ))
    coords_tot.append(coords)
    typ_tot.append(typ)

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
pts1.points = coords_tot[99]
txt.text(f"T=100")
plt.render()
plt.screenshot("s100.png")
plt.close()
