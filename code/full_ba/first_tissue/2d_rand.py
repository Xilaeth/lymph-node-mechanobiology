import sys 
import numpy as np
from random import random

x0 = 0
y0 = 0
z0 = 0
L = 10
N = 100
out = "out"

for inp in sys.argv[1:]:
    if (inp[0] == "-"):
        match inp[1:3]:
            case "x=":
                x0 = int(inp[3:])
                continue
            case "y=":
                y0 = int(inp[3:])
                continue
            case "z=":
                z0 = int(inp[3:])
                continue
            case "L=":
                L = float(inp[3:])
            case "N=":
                N = int(inp[3:])
    else:
        out = inp


data = []

for i in range(N):
    data.append([random()*L for i in range(3)])

leng = len(data)

with open(out + ".vtk", "w", encoding="ascii") as f:
    f.write("# vtk DataFile Version 3.0\n")
    f.write(out + "\n")
    f.write("ASCII\n")
    f.write("DATASET POLYDATA\n\n")
    f.write("POINTS " + str(leng) + " float\n")
    for i in data:
        f.write(str(i[0]) + " " + str(i[1]) + " " + "0.0\n")
