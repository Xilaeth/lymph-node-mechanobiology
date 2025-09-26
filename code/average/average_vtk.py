import numpy as np
import matplotlib.pyplot as plt
import sys

file_t = open(f"./out/{sys.argv[1]}-0.vtk", "rt")
content_t = file_t.read()
lines_t = content_t.splitlines()
lines_t = lines_t[6:]
n = len(lines_t)

out = np.zeros((n, 3))

for l in range(0, int(sys.argv[2])):
    file = open(f"./out/{sys.argv[1]}-{l}.vtk", "rt")
    content = file.read()
    lines = content.splitlines()
    lines = lines[6:]
    coords = np.array(list(map(lambda x: list(map(lambda y: float(y), x.split(' '))), lines)))
    out += coords 

with open(f"./out/{sys.argv[3]}.vtk", "w", encoding="ascii") as f:
    f.write("# vtk DataFile Version 3.0\n")
    f.write(f"{sys.argv[3]}" + "\n")
    f.write("ASCII\n")
    f.write("DATASET POLYDATA\n\n")
    f.write("POINTS " + str(len(out)) + " float\n")
    for i in out:
        f.write(str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + "\n")
