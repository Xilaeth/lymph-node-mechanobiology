import numpy as np
import sys

path = sys.argv[1]

coords = []

file = open(path)
content = file.read()
lines = content.splitlines()
lines = lines[6:]

for i in lines:
    if (not(i)):
        break;
    coords.append(i)

coords = np.array(list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords)))

xs = coords[:, 0]
ys = coords[:, 1]
zs = coords[:, 2]

xs.sort()
ys.sort()
zs.sort()

nt = int(len(xs))
n = int(0.05*nt)

x_avg_min = sum(xs[:n])
x_avg_max = sum(xs[(len(xs)-n):])
y_avg_min = sum(ys[:n])
y_avg_max = sum(ys[(len(ys)-n):])
z_avg_min = sum(zs[:n])
z_avg_max = sum(zs[(len(zs)-n):])
dx = x_avg_max - x_avg_min
dy = y_avg_max - y_avg_min
dz = z_avg_max - z_avg_min

print(dy/nt)
