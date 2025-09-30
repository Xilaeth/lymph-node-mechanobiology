import numpy as np
import sys

path1 = sys.argv[1]
path2 = sys.argv[2]
n = int(sys.argv[3])

coords1 = []
coords2 = []

file1 = open(path1)
file2 = open(path2)
content1 = file1.read()
content2 = file2.read()
lines1 = content1.splitlines()
lines2 = content2.splitlines()
lines1 = lines1[6:]
lines2 = lines2[6:]

for i in lines1:
    if (not(i)):
        break;
    coords1.append(i)

for i in lines2:
    if (not(i)):
        break;
    coords2.append(i)


coords1 = np.array(list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords1)))
coords2 = np.array(list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), coords2)))

disp = np.abs(coords1 - coords2)
mean_disp = np.mean(disp) / n

print(f"Average of the absolute displacement per bead: {mean_disp}")
