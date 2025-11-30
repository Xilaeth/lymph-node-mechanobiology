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

cr = []
cn = []
for i in range(len(coords_tot)):
    cr_temp = []
    cn_temp = []
    for j in range(len(coords_tot[0])):
        if (typ_tot[i][j] == 1):
            cr_temp.append(coords_tot[i][j])
        elif (typ_tot[i][j] == 2):
            cn_temp.append(coords_tot[i][j])
    cr.append(cr_temp)
    cn.append(cn_temp)

pts1 = Points(cr[0], r=6, c="green", alpha=1.0)
pts2 = Points(cn[0], r=6, c="blue", alpha=0.3)
txt = Text2D(txt="T=0", pos="top left").font("Calibri")

def slider(widget, event):
    pts1.points = cr[int(widget.value)]
    pts2.points = cn[int(widget.value)]
    txt.text(f"T={int(widget.value)}")

plt = Plotter()
plt.add_slider(slider, xmin=0, xmax=(len(coords_tot) - 1), value=0)
plt.show(pts1, pts2, txt, axes=1)
plt.interactive().close()
