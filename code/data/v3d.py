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

for i in lines:
    if (not(i)):
        break
    coords.append(i)

coords = list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords))


pts = Points(coords, r=4, c="green", alpha=1.0)

plt = Plotter()
plt.at(0).show(__doc__, pts)
plt.interactive().close()
