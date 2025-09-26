import sys 
import numpy as np

x0 = 0
y0 = 0
z0 = 0
nx = 100
ny = 100
nz = 100
l = 0.5
out = "out.vtk"

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
            case "l=":
                l = float(inp[3:])
        match inp[1:4]:
            case "nx=":
                nx = int(inp[4:])
                continue
            case "ny=":
                ny = int(inp[4:])
                continue
            case "nz=":
                nz = int(inp[4:])
                continue
    else:
        out = inp


def createRow(x, l, n):
    out = []
    for i in range(n):
        out.append([x[0] + i*l, x[1], x[2]])
    return out

def createSheet(x, l, nx, ny):
    out = []
    for i in range(ny):
        if ((i % 2) == 0):
            out.extend(createRow([x[0], x[1] + i*np.sin(np.pi/3)*l, x[2]], l, nx))
        if ((i % 2) == 1):
            out.extend(createRow([x[0] + np.cos(np.pi/3)*l, x[1] + i*np.sin(np.pi/3)*l, x[2]], l, nx))
    return out

def createRect(x, l, nx, ny, nz):
    out = []
    for i in range(nz):
        if ((i % 2) == 0):
            out.extend(createSheet([x[0], x[1], x[2] + i*np.sqrt(3)*l/2], l, nx, ny))
        if ((i % 2) == 1):
            out.extend(createSheet([x[0] + l/2, x[1] + np.sin(np.pi/3)*l/2, x[2] + i*np.sqrt(3)*l/2], l, nx, ny))
    return out

data = createRect([x0, y0, z0], l, nx, ny, nz)
leng = len(data)

with open(out, "w", encoding="ascii") as f:
    f.write("# vtk DataFile Version 3.0\n")
    f.write(out + "\n")
    f.write("ASCII\n")
    f.write("DATASET POLYDATA\n\n")
    f.write("POINTS " + str(leng) + " float\n")
    for i in data:
        f.write(str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + "\n")
