import os
import sys
from math import sqrt

load = "load.vtk"
a = 1.0
rmax = 1.0
T = 1000
dt = 0.05
every_n = 1
D = 0.01

for inp in sys.argv[1:]:
    if (inp[0] == '-'):
        match inp[1:3]:
            case "a=":
                a = inp[3:]
                continue
            case "rmax=":
                rmax = inp[3:]
                continue
            case "T=":
                T = inp[3:]
                continue
            case "D=":
                D = inp[3:]
                continue
        match inp[1:4]:
            case "dt=":
                dt = inp[4:]
                continue
            case "en=":
                every_n = inp[4:]
                continue
    else:
        load = inp

os.system(f"./load {load} {a} {rmax} {T} {dt} {every_n} {D}")
