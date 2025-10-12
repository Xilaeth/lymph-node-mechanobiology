# automatically creates the mask and density plots for all masks given a starting vtk

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from math import floor
import sys

file_name = "open.vtk"
mask_list = []


for inp in sys.argv[1:]:
    if (inp[0:4] == '-im='):
        mask_list.append(inp[4:])
    else:
        file_name = inp

# first we determine the approximate size of the tissue sample

file = open(sys.argv[1], "rt")
content = file.read()
lines = content.splitlines()
lines = lines[6:]

coords = list(map(lambda x: list(map(lambda y: float(y), x.split(' ')))[:2], lines))

xs = list(map(lambda x: x[0], coords))
ys = list(map(lambda x: x[1], coords))

def isInRect(x, lx, ly, v):
    if ((abs(v[0] - x[0]) < lx/2) and (abs(v[1] - x[1]) < ly/2)):
        return True
    return False

f1 = 1.0
f = 1.0

xop = f1 * max(xs)
yop = f1 * max(ys)
xom = f1 * min(xs)
yom = f1 * min(ys)
dx = xop - xom
dy = yop - yom
xc = xom + dx/2
yc = yom + dy/2
x = [xc, yc]
lx = f * dx
ly = f * dy


# generate the masked vtks for the masks and generate the corrosponding csv files
for inp in mask_list:

    x = [xc, yc]

    im = Image.open("../../../Data-2D/" + inp, 'r') 
    w, h = im.size
    if ((lx <= ly) and (lx*(h/w) > ly)):
        lx = ly * (w/h)
    elif ((lx <= ly) and (lx*(h/w) <= ly)):
        ly = lx *(h/w)
    elif ((ly < lx) and (ly*(w/h) > lx)):
        ly = lx * (h/w)
    elif ((ly < lx) and (ly*(w/h) <= lx)):
        lx = ly * (w/h)
    im_data = np.array(im)
    coordsOut = []

    for v in coords:
        if (not(isInRect(x, lx, ly, v))):
            continue
        px = floor((v[0] + (lx/2 - x[0]))*w/lx) - 1
        py = floor((v[1] + (ly/2 - x[1]))*h/ly) + 1
        if (im_data[h - py][px] != 0):
            coordsOut.append(v)

    xs = list(map(lambda x: x[0], coordsOut))
    ys = list(map(lambda x: x[1], coordsOut))

    leng = len(xs)
    out = "out_" + inp

    with open("output/" + out + ".vtk", "w", encoding="ascii") as f:
        f.write("# vtk DataFile Version 3.0\n")
        f.write(out + "\n")
        f.write("ASCII\n")
        f.write("DATASET POLYDATA\n\n")
        f.write("POINTS " + str(leng) + " float\n")
        for i in coordsOut:
            f.write(str(i[0]) + " " + str(i[1]) + " " + "0.0\n")
