import pyvista as pv
import numpy as np
import os
import sys

org = sys.argv[1]
folder = sys.argv[2]
out_name = sys.argv[3]
l = os.listdir(folder)

om = pv.read(org)
om_points = om.points

out = []

c = 0

for name in l:
    m = pv.read(folder + "/" + f"out-{c}_0.vtk")
    points = m.points
    d = np.array(points[c] - om_points[c])
    out.append(d)
    c += 1

with open(f"{out_name}.csv", "w", encoding="ascii") as f:
    for v in out:
        f.write(f"{v[0]},{v[1]},{v[2]}\n")
