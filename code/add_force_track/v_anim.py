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
    sc3 = 0
    for i in lines:
#        print(f"line: {i} | sc: {sc} | sc2: {sc2} | sc3: {sc3}")
        if (not(i) or (sc < 6 + len(coords) and sc>0)):
            sc += 1
        elif (((i[0] == 'S') or sc2>0) and sc2<2):
            sc2 += 1
        elif (((i[0] == 'S') or sc3>0) and sc3<2):
            sc3 += 1
        elif (sc == 0):
            coords.append(i)
        elif ((sc > 0) and (sc2==0)):
            continue
        elif ((sc2 > 0) and (sc3==0)):
            typ.append(i)
        elif (sc3 > 0):
            continue

    coords = list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords))
    typ = list(map(lambda x: int(x), typ))
    coords_tot.append(coords)
    typ_tot.append(typ)

#TextBase.font(font="Calibri")

pts1 = Points(coords_tot[0], r=6, c="green", alpha=1.0)
txt = Text2D(txt="T=0", pos="top left").font("Calibri")

def slider(widget, event):
    pts1.points = coords_tot[int(widget.value)]
    txt.text(f"T={int(widget.value)}")

plt = Plotter()
#ax = Axes(xygrid_transparent=True, title_font="Calibri", label_font="Calibri")
plt.add_slider(slider, xmin=0, xmax=(len(coords_tot) - 1), value=0)
plt.show(pts1, txt, axes=1)
plt.interactive().close()
