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

#TextBase.font(font="Calibri")

xs1 = list(map(lambda x: x[0], coords_tot[0]))
ys1 = list(map(lambda x: x[1], coords_tot[0]))
xs2 = list(map(lambda x: x[0], coords_tot[99]))
ys2 = list(map(lambda x: x[1], coords_tot[99]))

pts1 = Points(coords_tot[0], r=6, c="green", alpha=1.0)
txt = Text2D(txt="T=0", pos="top left").font("Calibri")

def slider(widget, event):
    pts1.points = coords_tot[int(widget.value)]
    txt.text(f"T={int(widget.value)}")

px = max(xs1)*1.1
py = max(ys1)*1.1
mx = min(xs1)*1.1
my = min(ys1)*1.1

plt = Plotter()
ax = Axes(xrange=(mx, px), yrange=(my, py), xygrid_transparent=True, title_font="Calibri", label_font="Calibri")
plt.show(pts1, ax, txt, interactive=False)
plt.screenshot(filename="0.png")
#px = max(xs2)*1.1
#py = max(ys2)*1.1
#mx = min(xs2)*1.1
#my = min(ys2)*1.1
#ax.xrange = (mx, px)
#ax.yrange = (my, py)
#pts1.points = coords_tot[99]
#txt.text("T=99")
#plt.render()
#plt.screenshot(filename="1.png")
plt.close()
