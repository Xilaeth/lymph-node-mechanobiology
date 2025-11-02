import os
import sys
from math import sqrt

load = "load.vtk"
a = 1.0
rmax = 1.0
T = 1000
dt = 0.01
every_n = 1
D = 0.01
f = 0.0
F = 1.0
F1 = 1.0
a1 = 1.0
fdir = 0
nr = 0

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
            case "F=":
                F = inp[3:]
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
            case "nr=":
                nr = int(inp[4:])
                continue
            case "F1=":
                F1 = float(inp[4:])
                continue
            case "a1=":
                a1 = float(inp[4:])
                continue
        match inp[1:6]:
            case "fdir=":
                fdir = int(inp[6:])
                continue
    else:
        load = inp

os.system(f"./small {load} {a} {rmax} {T} {dt} {every_n} {D} {F} {f} {fdir} {nr} {F1} {a1}")
