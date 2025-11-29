import os
import sys
from math import sqrt

load = "load.vtk"
a = 1.0
b = 1.0
T = 1000
dt = 0.01
every_n = 1
D = 0.01
f = 0.0
F1 = 1.0
a1 = 1.0
fdir = 0
nr = 0
frac = 1.0

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
            case "f=":
                f = inp[3:]
                continue
            case "b=":
                b = inp[3:]
                continue
        match inp[1:4]:
            case "dt=":
                dt = float(inp[4:])
                continue
            case "en=":
                every_n = int(inp[4:])
                continue
            case "nr=":
                nr = int(inp[4:])
                continue
            case "fr=":
                frac = int(inp[4:])
                continue
        match inp[1:6]:
            case "fdir=":
                fdir = int(inp[6:])
                continue
    else:
        load = inp

os.system(f"./small {load} {a} {dt} {T} {every_n} {D} {f} {fdir} {nr} {b} {frac}")
