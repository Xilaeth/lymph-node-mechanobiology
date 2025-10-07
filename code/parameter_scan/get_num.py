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

# to correct change the if statements

for i in lines:
    if (not(i)):
        continue
    if ((i[0] == "P") or ((sc < 2) and (sc>0))):
        sc += 1
        continue
    if ((i[0] == "P") or ((sc2 < 2) and (sc2>0))):
        sc2 += 1
        continue
    if (sc2 > 0):
        print(sc2)
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

print(n)
