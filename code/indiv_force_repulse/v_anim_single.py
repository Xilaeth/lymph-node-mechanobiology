import sys
import numpy as np
from vedo import *

path = sys.argv[1]
n = int(sys.argv[2])
fid = int(sys.argv[3])

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
        if (not(i) or ((sc < len(coords) + 6) and (sc > 0)) or (i[0] == 'S')):
            if (sc == (len(coords) + 6)):
                break
            sc += 1
            continue
        elif (sc == 0):
            coords.append(i)
        elif (sc > 0):
            typ.append(i)


    coords = list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords))
    typ = list(map(lambda x: int(x), typ))
    coords_tot.append(coords)
    typ_tot.append(typ)

pts1_tot = []
pts2_tot = []
pts3_tot = []


for f in range(len(coords_tot)):
    c = 0
    pts_tis = []
    pts_inb = []
    pt_fid = []

    for i in range(len(typ)):
        if (typ_tot[f][i] == 1):
            if (c == fid):
                pt_fid.append(coords_tot[f][i])
                c += 1
                continue
            pts_tis.append(coords_tot[f][i])
            c += 1
        if (typ_tot[f][i] == 2):
            pts_inb.append(coords_tot[f][i])

    pts1_tot.append(pts_tis)
    pts2_tot.append(pts_inb)
    pts3_tot.append(pt_fid)


pts1 = Points(pts1_tot[0], r=6, c="green", alpha=1.0)
pts2 = Points(pts2_tot[0], r=4, c=get_color(rgb=(190, 250, 215)), alpha=0.6)
pts3 = Points(pts3_tot[0], r=6, c="red", alpha=1.0)

def slider(widget, event):
    pts1.points = pts1_tot[int(widget.value)]
    pts2.points = pts2_tot[int(widget.value)]
    pts3.points = pts3_tot[int(widget.value)]

plt = Plotter(axes=1)
#plt.add_slider(slider, xmin=0, xmax=(len(coords_tot) - 1), value=0)
#plt.show(pts1, pts2, pts3)
plt.show(pts1, pts2, pts3, interactive=False)
#plt.interactive().close()
for i in range(100):
    pts1.points = pts1_tot[i]
    pts2.points = pts2_tot[i]
    pts3.points = pts3_tot[i]
    plt.screenshot(f"image{(i+1):03d}.png", scale=1)

plt.close()
