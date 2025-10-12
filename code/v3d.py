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


#pts.smooth_mls_2d(f=0.8)
#pts.subsample(0.005)
#reco = pts.reconstruct_surface(radius=0.5).c("green")
#m = Mesh(file_name, c='green')
#pts = Points(coords, r=6, c="green", alpha=1).density(radius=2, dims=(100, 100, 29)).smooth_gaussian(sigma=2)
#pts.cmap('coolwarm').alpha([0, 1])

#pts = Points(coords, r=6, c="green", alpha=0.02)
pts = Points(coords, r=6, c="green", alpha=1)

plt = Plotter().background(c1="white")
plt.at(0).show(__doc__, pts)
plt.interactive().close()
