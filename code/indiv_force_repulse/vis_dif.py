import os
import sys
import numpy as np
from vedo import *

file = open(sys.argv[1], "rt")
content = file.read()
lines = content.splitlines()
lines = lines[6:]

coords = []
fo = []

sc = 0
for i in lines:
    if (not(i) or (sc>0 and sc<4) or (i[0] == 'S')):
        if (sc == 4):
            break
        sc += 1
    elif (sc == 0):
        coords.append(i)
    elif (sc > 0):
        fo.append(i)   

coords = list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords))
fo = list(map(lambda x: int(x), fo))

coords_r = []

for i in range(len(coords)):
    if (fo[i] == 1):
        coords_r.append(coords[i])

file = sys.argv[2]

data = open(file)
content = data.read()
content = content.splitlines()
content = content[0::2]
content = list(map(lambda x: list(map(lambda y: y, x.split(' '))), content))
content = list(map(lambda x: [float(x[1]), float(x[4]), float(x[7])], content))
#content = list(map(lambda x: LA.norm(np.array(x)), content))
content = list(map(lambda x: x[0], content))

pts = Points(coords_r, r=6, c='green', alpha=1.0)
pts.pointdata["deformation"] = content
pts.cmap("coolwarm").add_scalarbar("deformation")

plt = Plotter()
plt.show(pts).interactive().close()
