import sys
import numpy as np
from vedo import *

file_name = "load.vtk"

for inp in sys.argv:
    if (inp[0] == "-"):
        print(":)")
    else:
        file_name = inp

file = open(file_name)
content = file.read()
lines = content.splitlines()
lines = lines[6:]

coords = []
typ = []

sc = 0
for i in lines:
    if (not(i) or ((sc < 4) and (sc > 0))):
        sc += 1
        continue
    if (sc == 0):
        coords.append(i)
    if (sc > 0):
        typ.append(i)

print(typ)

coords = list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords))
typ = list(map(lambda x: int(x), typ))

xs = list(map(lambda x: x[0], coords))
ys = list(map(lambda x: x[1], coords))

pts_tis = []
pts_inb = []

for i in range(len(typ)):
    if (typ[i] == 1):
        pts_tis.append(coords[i])
    if (typ[i] == 2):
        pts_inb.append(coords[i])

pts1 = Points(pts_tis, r=4, c="green", alpha=1.0)
pts2 = Points(pts_inb, r=4, c=get_color(rgb=(190, 250, 215)), alpha=0.7)

plt = Plotter()
plt.at(0).show(__doc__, pts1, pts2)
plt.interactive().close()
