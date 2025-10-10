import os
import sys

f1 = "load.vtk"
f2 = "load2.vtk"
n = 0

for inp in sys.argv:
    if (inp[0] == "-"):
        match inp[1:3]:
            case "n=":
                n = int(inp[3:])
                continue
        match inp[1:4]:
            case "f1=":
                f1 = inp[4:]
                continue
            case "f2=":
                f2 = inp[4:]
                continue

file1 = open(f1)
file2 = open(f2)
content1 = file1.read()
content2 = file2.read()
lines1 = content1.splitlines()
lines2 = content2.splitlines()
lines1 = lines1[6:]
lines2 = lines2[6:]

coords1 = []
typ1 = []

sc = 0
for i in lines1:
    if (not(i) or ((sc < (6 + len(coords1))) and (sc > 0))):
        sc += 1
        continue
    if (sc == 0):
        coords1.append(i)
    if (sc > 0):
        typ1.append(i)

coords2 = []
typ2 = []

sc = 0
for i in lines2:
    if (not(i) or ((sc < (6 + len(coords2))) and (sc > 0))):
        sc += 1
        continue
    if (sc == 0):
        coords2.append(i)
    if (sc > 0):
        typ2.append(i)

coords1 = list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords1))
typ1 = list(map(lambda x: int(x), typ1))
coords2 = list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords2))
typ2 = list(map(lambda x: int(x), typ2))

i1 = typ1.index(n)
i2 = typ2.index(n)

dx = coords2[i2][0] - coords1[i1][0]
dy = coords2[i2][1] - coords1[i1][1]
dz = coords2[i2][2] - coords1[i1][2]

print(dx, " ", dy, " ", dz)
