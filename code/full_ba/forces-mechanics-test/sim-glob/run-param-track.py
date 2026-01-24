import os
import sys
from math import sqrt

load = "load.vtk"
a = 1.0
b = 1.0
d = 2.0
req = 1.0
T = 1000
dt = 0.01
every_n = 1
D = 0.01
f = 0.0
f_dir = 0
ids = 1

for inp in sys.argv[1:]:
    if (inp[0] == '-'):
        match inp[1:3]:
            case "a=":
                a = inp[3:]
                continue
            case "T=":
                T = inp[3:]
                continue
            case "D=":
                D = inp[3:]
                continue
            case "b=":
                b = inp[3:]
                continue
            case "d=":
                d = inp[3:]
                continue
            case "f=":
                f = inp[3:]
                continue
        match inp[1:4]:
            case "dt=":
                dt = float(inp[4:])
                continue
            case "en=":
                every_n = int(inp[4:])
                continue
            case "fd=":
                f_dir = int(inp[4:])
                continue
            case "id=":
                ids = int(inp[4:])
                continue
        match inp[1:5]:
            case "req=":
                req = float(inp[5:])
                continue
    else:
        load = inp

os.system(f"./track {load} {a} {b} {d} {req} {dt} {T} {every_n} {D} {f} {f_dir} {ids}")
