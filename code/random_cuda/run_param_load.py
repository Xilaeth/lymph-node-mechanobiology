import os
import sys
from math import sqrt

load = sys.argv[1]
a = sys.argv[2]
rmax = sys.argv[3]
T = sys.argv[4]
dt = sys.argv[5]
every_n = sys.argv[6]
D = sys.argv[7]

os.system(f"./load {load} {a} {rmax} {T} {dt} {every_n} {D}")
