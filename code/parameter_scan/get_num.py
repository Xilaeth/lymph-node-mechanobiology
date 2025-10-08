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
    if (not(i)):
        continue
    if (((i[0] == "P") and sc==0) or ((sc < 3) and (sc>0))):
        sc += 1
        continue
    if (((i[0] == "P") and sc2==0) or ((sc2 < 3) and (sc2>0))):
        sc2 += 1
        continue
    if (sc2 > 0):
        typ.append(i)
        continue
    elif (sc > 0):
        f.append(i) 
        continue
    elif (sc == 0):
        coords.append(i)
        continue

f = list(map(lambda x: int(x), f))
f = list(map(lambda x: 1 if (x == 3) else 0, f))
n = sum(f)

#typ = list(map(lambda x: int(x), typ))
#typ = list(map(lambda x: 1 if (x == 1) else 0, typ))
#n = sum(typ)

print(n)
