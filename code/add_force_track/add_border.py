import sys
import numpy as np

file = open(sys.argv[1], "rt")
content = file.read()
lines = content.splitlines()
lines = lines[6:]

coords = []

sc = 0
for i in lines:
    if (not(i)):
        break
    if (sc == 0):
        coords.append(i)

coords = list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords))

xs = list(map(lambda x: x[0], coords))
ys = list(map(lambda x: x[1], coords))

fxs = 0
fxe = 1
fys = 0
fye = 1

xop = max(xs)
yop = max(ys)
xom = min(xs)
yom = min(ys)
dx = xop - xom
dy = yop - yom
xc = xom + dx/2
yc = yom + dy/2
x = [xc, yc]
lx = dx
ly = dy
