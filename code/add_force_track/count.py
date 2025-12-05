import os
import sys
import numpy as np

file = open(sys.argv[1], "rt")
content = file.read()
lines = content.splitlines()
lines = lines[6:]

fo = []

sc = 0
sc2 = 0
sc3 = 0
for i in lines:
#    print(f"line: {i} | sc: {sc} | sc2: {sc2} | sc3: {sc3}")
    if ((not(i) or sc>0) and sc<4):
        sc += 1
    elif ((not(i) or sc2>0) and sc2<4):
        sc2 += 1
    elif ((not(i) or sc3>0) and sc3<4):
        sc3 += 1
    elif (sc == 0):
        continue
    elif ((sc > 0) and (sc2==0)):
        continue
    elif ((sc2 > 0) and (sc3==0)):
        fo.append(i)
    elif (sc3 > 0):
        continue

fo = list(map(lambda x: int(x), fo))

n = sum(list(map(lambda x: 1 if x == 1 else 0, fo)))
print(n)
