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
fxl = 0.0
fxr = 0.0
fyu = 0.0
fyd = 0.0
fxyur = 0.0
fxyul = 0.0
fxydr = 0.0
fxydl = 0.0

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
                fxl = float(inp[3:])
                fxr = float(inp[3:])
                fyu = float(inp[3:])
                fyd = float(inp[3:])
                fxyul = float(inp[3:])
                fxyur = float(inp[3:])
                fxydl = float(inp[3:])
                fxydr = float(inp[3:])
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
        match inp[1:5]:
            case "fxl=":
                fxl = float(inp[5:])
                continue
            case "fxr=":
                fxr = float(inp[5:])
                continue
            case "fyu=":
                fyu = float(inp[5:])
                continue
            case "fyd=":
                fyd = float(inp[5:])
                continue
        match inp[1:7]:
            case "fxyul=":
                fxyul = float(inp[7:])
                continue
            case "fxyur=":
                fxyur = float(inp[7:])
                continue
            case "fxydl=":
                fxydl = float(inp[7:])
                continue
            case "fxydr=":
                fxydr = float(inp[7:])
    else:
        load = inp

os.system(f"./load {load} {a} {rmax} {T} {dt} {every_n} {D} {fxr} {fxl} {fyu} {fyd} {fxyur} {fxyul} {fxydr} {fxydl}")
