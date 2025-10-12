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

xs = list(map(lambda x: x[0], coords_tot[0]))
ys = list(map(lambda x: x[1], coords_tot[0]))

pts1 = Points(coords_tot[0], r=6, c="green", alpha=1.0)
txt = Text2D(txt="T=0", pos="top left").font("Calibri")

def slider(widget, event):
    pts1.points = coords_tot[int(widget.value)]
    txt.text(f"T={int(widget.value)}")

px = max(xs) 
mx = min(xs)
py = max(ys)
my = min(ys)
dx = px - mx
dy = py - my
px += 0.05*dx
mx -= 0.05*dx
py += 0.05*dy
my -= 0.05*dy

plt = Plotter()
ax = Axes(xrange=(mx, px), yrange=(my, py), xygrid_transparent=True, title_font="Calibri", label_font="Calibri")
plt.add_slider(slider, xmin=0, xmax=(len(coords_tot) - 1), value=0)
plt.show(pts1, ax, txt, interactive=True).close()
#plt.screenshot(filename="0.png")
#pts1.points = coords_tot[99]
#txt.text("T=99")
#plt.screenshot(filename="1.png")
