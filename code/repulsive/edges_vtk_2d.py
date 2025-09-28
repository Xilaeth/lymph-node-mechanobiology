import os
import sys
import numpy as np

file = open(sys.argv[1], "rt")
content = file.read()
lines = content.splitlines()
lines = lines[6:]

coords = []
typ_v = []

sc = 0
for i in lines:
    if (not(i) or ((sc < 4) and (sc > 0))):
        sc += 1
        continue
    if (sc == 0):
        coords.append(i)
    if (sc > 0):
        typ_v.append(i)

coords = list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords))
typ_v = list(map(lambda x: int(x), typ_v))

xs = list(map(lambda x: x[0], coords))
ys = list(map(lambda x: x[1], coords))

f1 = float(sys.argv[3])
f = float(sys.argv[4])
fm = 1 - f

xop = f1*max(xs)
yop = f1*max(ys)
xom = f1*min(xs)
yom = f1*min(ys)
dx = xop - xom
dy = yop - yom
xc = xom + dx/2
yc = yom + dy/2
x = [xc, yc]
lx = f*dx
ly = f*dy
l = min(lx, ly)

typ = []
ind = -1

for i in coords:
    ind += 1
    if (typ_v[ind] == 2):
        typ.append(0)
        continue
    if ((i[0] < (xom + fm*l)) or (i[0] > (xop - fm*l)) or (i[1] < (yom + fm*l)) or (i[1] > (yop - fm*l))):
        if (i[0] < (xom + fm*l)):
            if (i[1] < (yom + fm*l)):
                typ.append(5)
            elif (i[1] > (yop - fm*l)):
                typ.append(6)
            else:
                typ.append(1)
        else:
            if (i[0] > (yop - fm*l)):
                if (i[1] < (yom + fm*l)):
                    typ.append(8)
                elif (i[1] > (yop - fm*l)):
                    typ.append(7)
                else:
                    typ.append(3)
            else:
                if (i[1] < (yom + fm*l)):
                    typ.append(4)
                else:
                    typ.append(2)
    else:
        typ.append(0)

out = sys.argv[2]
leng = len(coords)

with open(f"{out}.vtk", "w", encoding="ascii") as f:
    f.write("# vtk DataFile Version 3.0\n")
    f.write(out + "\n")
    f.write("ASCII\n")
    f.write("DATASET POLYDATA\n\n")
    f.write("POINTS " + str(leng) + " float\n")
    for i in coords:
        f.write(str(i[0]) + " " + str(i[1]) + " 0.0\n")
    f.write("\nPOINT_DATA " + str(leng) + "\n")
    f.write("SCALARS vf float\n")
    f.write("LOOKUP_TABLE default\n")
    for i in typ:
        f.write(str(i) + "\n")
    f.write("\nPOINT_DATA " + str(leng) + "\n")
    f.write("SCALARS v float\n")
    f.write("LOOKUP_TABLE default\n")
    for i in typ_v:
        f.write(str(i) + "\n")
