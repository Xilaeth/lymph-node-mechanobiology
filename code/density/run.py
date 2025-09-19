import os
import sys

l = 82 * 0.9
n = 100
r = 2
xc = 44.5
yc = 38.5
name = sys.argv[1]

os.system(f"./density out_vtks/{name}.vtk {l} {n} {r} out_vtks/{name}.csv {xc} {yc}")
