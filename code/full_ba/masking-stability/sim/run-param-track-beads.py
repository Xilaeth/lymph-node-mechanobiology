import os
import sys
from math import sqrt

load = "load.vtk"
a = 0.2
b = 1.0
a2 = 0.1
d = 2.0
req = 1.0
T = 1000
dt = 0.01
every_n = 1
D = 0.01

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
        match inp[1:4]:
            case "dt=":
                dt = float(inp[4:])
                continue
            case "en=":
                every_n = int(inp[4:])
                continue
            case "a2=":
                a2 = float(inp[4:]) 
                continue
        match inp[1:5]:
            case "req=":
                req = float(inp[5:])
                continue
    else:
        load = inp

os.system(f"./track-beads {load} {a} {b} {d} {req} {dt} {T} {every_n} {D} {a2}")
