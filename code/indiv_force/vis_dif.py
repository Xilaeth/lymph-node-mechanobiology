import numpy as np
import sys
from vedo import * 
from numpy import linalg as LA

vtk = sys.argv[1]

vtk_file = open(vtk)
content_vtk = vtk_file.read()
lines_vtk = content_vtk.splitlines()
lines_vtk = lines_vtk[6:]

coords = []

for i in lines_vtk:
    if (not(i)):
        break
    coords.append(i)

coords = np.array(list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords)))

file = sys.argv[2]

data = open(file)
content = data.read()
content = content.splitlines()
content = content[0::2]
content = list(map(lambda x: list(map(lambda y: y, x.split(' '))), content))
content = list(map(lambda x: [float(x[1]), float(x[4]), float(x[7])], content))
#content = list(map(lambda x: LA.norm(np.array(x)), content))
content = list(map(lambda x: x[0], content))

pts = Points(coords, r=6, c='green', alpha=1.0)
pts.pointdata["deformation"] = content
pts.cmap("coolwarm").add_scalarbar("deformation")

plt = Plotter()
plt.show(pts).interactive().close()
