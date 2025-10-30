import os
import sys
import numpy as np

file = 'input.tif'
a = ":)"

for inp in sys.argv[1:]:
    if (inp[0] == '-'):
        match inp[1:3]:
            case "a=":
                a = inp[3:]
                continue
    else:
        file = inp

file_o = open(sys.argv[1], "rt")
content = file_o.read()
lines = content.splitlines()
lines = lines[6:]
coords = []
xs, ys, zs = [], [], []

shift = 6
shifts = 1

sc = 0
sc2 = 0
sc3 = 0
sc4 = 0
l = 0
for i in lines:
    if (not(i) and (sc == 0)):
        sc += 1
        continue
    elif (sc == 0):
        l += 1
    elif ((sc > 0) and (sc2 == 0)):
        sc += 1
        if (sc < l):
            continue
        if (sc < l + shift):
            continue
        if (sc == l + shift):
            l += 2
            sc2 = 1
            continue
    elif ((sc2 > 0) and (sc3 == 0)):
        sc2 += 1
        if (sc2 < l):
            xs.append(float(i))
            continue
        if (sc2 < l + shifts):
            continue
        if (sc2 == l + shifts):
            sc3 = 1
            continue
    elif ((sc3 > 0) and (sc4 == 0)):
        sc3 += 1
        if (sc3 < l):
            ys.append(float(i))
            continue
        if (sc3 < l + shifts):
            continue
        if (sc3 == l + shifts):
            sc4 = 1
            continue
    elif ((sc4 > 0)):
        sc4 += 1
        if (sc4 < l):
            zs.append(float(i))
            continue

with open(f"data.csv", "w", encoding="ascii") as f:
    for i in range(len(xs)):
        f.write(f"{xs[i]},{ys[i]},{zs[i]}\n")
