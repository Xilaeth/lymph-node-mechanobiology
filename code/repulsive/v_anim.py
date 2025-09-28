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
    for i in lines:
        if (not(i) or ((sc < 6 + len(coords)) and (sc > 0))):
            sc += 1
            continue
        if (sc == 0):
            coords.append(i)
        if (sc > 0):
            typ.append(i)

    coords = list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords))
    typ = list(map(lambda x: int(x), typ))
    coords_tot.append(coords)
    typ_tot.append(typ)

pts1_tot = []
pts2_tot = []

for f in range(len(coords_tot)):
    pts_tis = []
    pts_inb = []

    for i in range(len(typ)):
        if (typ_tot[f][i] == 1):
            pts_tis.append(coords_tot[f][i])
        if (typ_tot[f][i] == 2):
            pts_inb.append(coords_tot[f][i])

    pts1_tot.append(pts_tis)
    pts2_tot.append(pts_inb)

pts1 = Points(pts1_tot[0], r=4, c="green", alpha=1.0)
pts2 = Points(pts2_tot[0], r=4, c=get_color(rgb=(190, 250, 215)), alpha=0.7)

def slider(widget, event):
    pts1.points = pts1_tot[int(widget.value)]
    pts2.points = pts2_tot[int(widget.value)]

plt = Plotter()
plt.add_slider(slider, xmin=0, xmax=(len(coords_tot) - 1), value=0)
plt.show(pts1, pts2)
plt.interactive().close()
