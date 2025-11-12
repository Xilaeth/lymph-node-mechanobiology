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

coords_r = np.array(coords_r)

lx = max(coords_r[:, 0]) - min(coords_r[:, 0])
ly = max(coords_r[:, 1]) - min(coords_r[:, 1])
mx = min(coords_r[:, 0])
my = min(coords_r[:, 1])
file = sys.argv[2]

content = np.loadtxt(sys.argv[2], delimiter=',')
indeces = []
for i in range(len(content)):
    if (content[i][0] == 1000):
        indeces.append(i)
content = np.delete(content, indeces, axis=0)

#content = list(map(lambda x: LA.norm(np.array(x)), content))
content = list(map(lambda x: x[0], content))

ps = []
cs = []
o = []
frac = 0.95
for i in range(len(coords_r)):
    if ((np.abs(coords_r[i, 0] - (mx + lx/2)) < 0.5*frac*lx) and (np.abs(coords_r[i, 1] - (my + ly/2)) < 0.5*frac*ly)):
        ps.append(coords_r[i])
        cs.append(content[i])
    else:
        o.append(coords_r[i])

pts = Points(ps, r=6, c='green', alpha=1.0)
pts_o = Points(o, r=6, c='black', alpha=0.5)
pts.pointdata["deformation"] = cs
pts.cmap("coolwarm").add_scalarbar("deformation")

plt = Plotter()
plt.show(pts, pts_o).close()

