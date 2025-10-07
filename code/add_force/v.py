import sys
import numpy as np
from vedo import *

coords_tot = []
typ_tot = []

file = open(f"{sys.argv[1]}.vtk")
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
        continue
    if (sc > 0):
        continue


coords = list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords))

xs = list(map(lambda x: x[0], coords))
ys = list(map(lambda x: x[1], coords))

pts1 = Points(coords, r=6, c="green", alpha=1.0)

px = max(xs)*1.1
py = max(ys)*1.1
mx = min(xs)*1.1
my = min(ys)*1.1

plt = Plotter()
ax = Axes(xrange=(mx, px), yrange=(my, py), xygrid_transparent=True, title_font="Calibri", label_font="Calibri")
plt.show(pts1, ax, interactive=False)
plt.screenshot(filename="0.png")
plt.close()
