import os
import sys
from math import sqrt

load = "load.vtk"
a = 1.0
rmax = 1.0
T = 1000
dt = 0.01
every_n = 1
F = 1.0
f = 0.0

for inp in sys.argv[1:]:
    if (inp[0] == '-'):
        match inp[1:3]:
            case "a=":
                a = inp[3:]
                continue
            case "T=":
                T = inp[3:]
                continue
            case "F=":
                F = inp[3:]
                continue
            case "f=":
                f = float(inp[3:])
                continue
        match inp[1:4]:
            case "rm=":
                rmax = float(inp[4:])
                continue
            case "dt=":
                dt = float(inp[4:])
                continue
            case "en=":
                every_n = int(inp[4:])
                continue
    else:
        load = inp

os.system(f"./load {load} {a} {rmax} {T} {dt} {every_n} {F} {f}")
