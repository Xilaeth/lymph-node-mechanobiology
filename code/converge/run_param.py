import os
import sys
from math import sqrt

n = float(sys.argv[1])
a = sys.argv[2]
rmax = sys.argv[3]
rect = sqrt(n)
T = sys.argv[4]
dt = sys.argv[5]
every_n = sys.argv[6]
starting_dist = sys.argv[7]

os.system(f"./relax {n} {a} {rmax} {rect} {T} {dt} {every_n} {starting_dist}")
