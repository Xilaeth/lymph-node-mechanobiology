import sys
from vedo import *
import numpy as np
from numpy import linalg as LA
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt

file_name_1 = "before.vtk"
file_name_2 = "after.vtk"

for inp in sys.argv:
    if (inp[0] == "-"):
        match inp[1:3]:
            case "b=":
                file_name_1 = inp[3:]
                continue
            case "a=":
                file_name_2 = inp[3:]
                continue
    else:
        continue

file1 = open(file_name_1)
content1 = file1.read()
file2 = open(file_name_2)
content2 = file2.read()
lines1 = content1.splitlines()
lines1 = lines1[6:]
lines2 = content2.splitlines()
lines2 = lines2[6:]

coords1 = []
typ1 = []

sc = 0
sc2 = 0
for i in lines1:
    if (not(i) or ((sc < 4) and (sc > 0))):
        sc += 1
        continue
    if (sc == 0):
        coords1.append(i)
    if ((i[0] == "S") or ((sc2 < 2) and (sc2>0))):
        sc2 += 1
        continue
    if (sc2 > 0):
        typ1.append(i)
    if (sc > 0):
        continue

coords1 = np.array(list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords1)))
typ1 = list(map(lambda x: int(x), typ1))

prop_coords1 = []
for i in range(len(coords1)):
    if (typ1[i] == 1):
        prop_coords1.append(coords1[i])
prop_coords1 = np.array(prop_coords1)

coords2 = []
typ2 = []

sc = 0
sc2 = 0
for i in lines2:
    if (not(i) or ((sc < 4) and (sc > 0))):
        sc += 1
        continue
    if (sc == 0):
        coords2.append(i)
    if ((i[0] == "S") or ((sc2 < 2) and (sc2>0))):
        sc2 += 1
        continue
    if (sc2 > 0):
        typ2.append(i)
    if (sc > 0):
        continue

coords2 = np.array(list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords2)))
typ2 = list(map(lambda x: int(x), typ2))

prop_coords2 = []
for i in range(len(coords2)):
    if (typ2[i] == 1):
        prop_coords2.append(coords2[i])
prop_coords2 = np.array(prop_coords2)

disp = prop_coords2 - prop_coords1


prop_coords1 = np.array(list(map(lambda x: x[:2], prop_coords1)))
data = prop_coords1.transpose()

f1 = 1.0
f = 1.0
fm = 1 - f

xs = list(map(lambda x: x[0], prop_coords1))
ys = list(map(lambda x: x[1], prop_coords1))

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

dens = gaussian_kde(data)

N = 100

dx = lx/N
dy = ly/N

xs_out = []
ys_out = []
vals_out = []

for x in range(N):
    for y in range(N):
        xs_out.append(x)
        ys_out.append(y)
        vals_out.append(dens.evaluate([x*dx, y*dy])[0])

xs_out = np.array(xs_out)
ys_out = np.array(ys_out)
vals_out = np.array(vals_out)

nx = xs_out.max() + 1
ny = ys_out.max() + 1

grid = np.full((ny, nx), np.nan)

for x, y, v in zip(xs_out, ys_out, vals_out):
    grid[y, x] = v

fig, ax = plt.subplots()
ax.imshow(grid, origin='lower', cmap='Greens', interpolation='none')

ax.set_axis_off()

plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

plt.show()
