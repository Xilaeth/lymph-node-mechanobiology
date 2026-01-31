import sys
import numpy as np
import pyvista as pv
from vedo import *

path = sys.argv[1]
n = int(sys.argv[2])

coords_tot = []
typ_tot = []

for i in range(n):
    m = pv.read(f"{path}{i}.vtk")
    pos = m.points

    coords_tot.append(pos)

pts1 = Points(coords_tot[0], r=10, c="green", alpha=1.0)
txt = Text2D(txt="T=0", pos="top left").font("Calibri")

def slider(widget, event):
    pts1.points = coords_tot[int(widget.value)]
    txt.text(f"T={int(widget.value)}")

plt = Plotter()
#ax = Axes(xygrid_transparent=True, title_font="Calibri", label_font="Calibri")
plt.add_slider(slider, xmin=0, xmax=(len(coords_tot) - 1), value=0)
plt.show(pts1, txt, axes=1)
plt.interactive().close()
