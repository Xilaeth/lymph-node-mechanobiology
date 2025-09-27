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

coords = list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords))
typ = list(map(lambda x: int(x), typ))

coords_n = []
coords_f = []

for i in range(len(coords)):
    if (typ[i] == 0):
        coords_n.append(coords[i])
    else:
        coords_f.append(coords[i])

pts_n = Points(coords_n).ps(10).c("green")
pts_f = Points(coords_f).ps(10).c("red")

plt = Plotter()
plt.at(0).show(__doc__, pts_t_n, pts_t_f)
plt.interactive()
plt.close()
