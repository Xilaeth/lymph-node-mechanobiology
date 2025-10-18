import os
import sys
import numpy as np

file = open(sys.argv[1], "rt")
content = file.read()
lines = content.splitlines()
lines = lines[6:]

fo = []

sc = 0
for i in lines:
    if (not(i) or (sc>0 and sc<4)):
        sc += 1
    elif (sc == 0):
        continue
    elif (sc > 0):
        fo.append(i)   

fo = list(map(lambda x: int(x), fo))

n = list(map(lambda x: 1 if x == 1 else 0, fo))
print(n)
