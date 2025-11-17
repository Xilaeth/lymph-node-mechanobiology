import os
import sys
import numpy as np
from vedo import *

file1 = 'input.tif'
file2 = 'input.csv'
a = ":)"

for inp in sys.argv[1:]:
    if (inp[0] == '-'):
        match inp[1:4]:
            case "f1=":
                file1 = inp[4:]
                continue
        match inp[1:4]:
            case "f2=":
                file2 = inp[4:]
                continue
    else:
        continue

file1_o = open(file1, "rt")
content1 = file1_o.read()
lines1 = content1.splitlines()
lines1 = lines1[6:]
coords = np.array(list(map(lambda x: list(map(float, x.split(' '))), lines1)))

file2_o = open(file2, "rt")
content2 = file2_o.read()
lines2 = content2.splitlines()
disp = np.array(list(map(lambda x: list(map(float, x.split(' '))), lines2)))
cs = disp[:, 0]

pts = Points(coords, r=6, c='green', alpha=1.0)
pts.pointdata["deformation"] = cs
pts.cmap("coolwarm").add_scalarbar("deformation")

plt = Plotter()
plt.show(pts).close()
