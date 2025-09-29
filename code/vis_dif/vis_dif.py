import sys
from vedo import *
import numpy as np
from numpy import linalg as LA

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
max_mag = max(list(map(lambda x: LA.norm(x), disp)))
disp /= max_mag
disp *= 1

pts_ini = Points(prop_coords1, r=4, c="green", alpha=0.3)
#arr = Arrows(prop_coords1, prop_coords1 + disp, thickness=0.5, c="coolwarm")
arr = Arrows(prop_coords1, prop_coords1 + disp, thickness=0.5, c="black")

plt = Plotter()
plt.show(pts_ini, arr).interactive().close()
