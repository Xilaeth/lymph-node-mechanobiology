import sys
import numpy as np
import pyvista as pv
from vedo import *

path = sys.argv[1]
n = int(sys.argv[2])
p = int(sys.argv[3])

coords_tot = []
typ_tot = []

for i in range(n):
    m = pv.read(f"{path}{i}.vtk")
    pos = m.points

    coords_tot.append(pos)

pts1_tot = []
pts2_tot = []

for i in range(len(coords_tot)):
    pts1_temp = []
    pts2_temp = []
    for j in range(len(coords_tot[0])):
        if (j == p):
            pts2_temp.append(coords_tot[i][j])
        else:
            pts1_temp.append(coords_tot[i][j])
    pts1_tot.append(pts1_temp)
    pts2_tot.append(pts2_temp)

pts1 = Points(pts1_tot[0], r=10, c="green", alpha=1.0)
pts2 = Points(pts2_tot[0], r=10, c="red", alpha=1.0)
txt = Text2D(txt="T=0", pos="top left").font("Calibri")

def slider(widget, event):
    pts1.points = pts1_tot[int(widget.value)]
    pts2.points = pts2_tot[int(widget.value)]
    txt.text(f"T={int(widget.value)}")

plt = Plotter()
#ax = Axes(xygrid_transparent=True, title_font="Calibri", label_font="Calibri")
plt.add_slider(slider, xmin=0, xmax=(len(coords_tot) - 1), value=0)
plt.show(pts1, pts2, txt, axes=1)
plt.interactive().close()
