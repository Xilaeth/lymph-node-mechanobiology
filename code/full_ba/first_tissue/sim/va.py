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
sc2 = 0
for i in lines:
    if (not(i) or ((sc < 4) and (sc > 0))):
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

pts = Points(coords, r=4, c="green", alpha=1.0)

plt = Plotter()
plt.at(0).show(__doc__, pts)
plt.interactive().close()
