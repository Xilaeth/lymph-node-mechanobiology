import sys
import numpy as np

coords_tot = []
typ_tot = []

file = open(f"{sys.argv[1]}.vtk")
content = file.read()
lines = content.splitlines()
lines = lines[6:]

coords = []
typ = []
f = []

sc = 0
sc2 = 0
for i in lines:
    if ((i[0] == "S") or ((sc < 2) and (sc>0))):
        sc += 1
        continue
    if ((i[0] == "S") or ((sc2 < 2) and (sc2>0))):
        sc2 += 1
        continue
    if (sc == 0):
        coords.append(i)
    if (sc > 0):
        f.append(i) 
    if (sc2 > 0):
        typ.append(i)

f = list(map(lambda x: int(x), f))
f = list(map(lambda x: 1 if (x == 3) else 0, f))
n = sum(f)

print(f)
