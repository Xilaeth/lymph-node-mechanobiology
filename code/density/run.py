import os
import sys

l = 82 * 0.9
n = 100
r = 2
xc = 44.5
yc = 38.5
name = sys.argv[1]

os.system(f"./density {name}.vtk {l} {n} {r} {name}.csv {xc} {yc}")
