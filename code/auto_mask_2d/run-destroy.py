# automatically creates the mask and density plots for all masks given a starting vtk

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from math import floor

# first we determine the approximate size of the tissue sample

file = open(sys.argv[1], "rt")
content = file.read()
lines = content.splitlines()
lines = lines[6:]

coords = list(map(lambda x: list(map(lambda y: float(y), x.split(' ')))[:2], lines))

xs = list(map(lambda x: x[0], coords))
ys = list(map(lambda x: x[1], coords))

def isInSquare(x, l, v):
    if ((abs(v[0] - x[0]) < l/2) and (abs(v[1] - x[1]) < l/2)):
        return True
    return False

def isInCirc(x, r, v):
    if ((v[0] - x[0])**2 + (v[1] - x[1])**2 < r**2):
        return True
    return False

def densityInCirc(x, r):
    counter = 0
    for i in range(len(xs)):
        if (isInCirc(x, r, coords[i])):
            counter += 1
    return (counter / (np.pi*r*r))

xop = 0.98 * max(xs)
yop = 0.98 * max(ys)
xom = 0.98 * min(xs)
yom = 0.98 * min(ys)
dx = xop - xom
dy = yop - yom
xc = xom + dx/2
yc = yom + dy/2
x = [xc, yc]
l = 0.95*min(dx, dy)

# generate the csv for the original file and the corrosponding density plot
#os.system(f"./density {sys.argv[1]} {l} {sys.argv[2]} {sys.argv[3]} output/out_original.csv {xc} {yc}")

#data = np.loadtxt("output/out_original.csv", delimiter=",")

#arr = np.array(data)
#xs = arr[:,0].astype(int)
#ys = arr[:,1].astype(int)
#vals = arr[:,2]

#nx = xs.max() + 1
#ny = ys.max() + 1

#grid = np.full((ny, nx), np.nan)
#
#for x, y, v in zip(xs, ys, vals):
#    grid[y, x] = v
#
#fig, ax = plt.subplots()
#ax.set_axis_off()
#ax.set_box_aspect(1)
#plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
#ax.imshow(grid, origin='lower', cmap='Greens', interpolation='none')
#plt.savefig(f"output/out_original_density.png", bbox_inches='tight')

mask_list = ["hole", "lines", "small_lines", "small_holes", "medium_holes"] #["lines_random_create", "lines_vertical_create"]

# generate the masked vtks for the masks and generate the corrosponding csv files
for inp in mask_list:

    x = [xc, yc]

    im = Image.open("../pngs/" + inp + ".png", 'r') 
    width, height = im.size
    pixel_values = list(im.getdata())
    pixel_values = np.array(pixel_values).reshape((width, height, 4))
    coordsOut = []

    for v in coords:
        if (not(isInSquare(x, l, v))):
        #    coordsOut.append(v)
            continue
        px = floor((v[0] + (l/2 - x[0]))*500/l)
        py = floor((v[1] + (l/2 - x[1]))*500/l)
        if (pixel_values[px][py][0] != 0):
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
    
#    os.system(f"./density output/{out + '.vtk'} {l} {sys.argv[2]} {sys.argv[3]} output/{out + '.csv'} {xc} {yc}")
#
#    data = np.loadtxt("output/" + out + '.csv', delimiter=",")
#
#    # Convert to array for easier manipulation
#    arr = np.array(data)
#    xs = arr[:,0].astype(int)
#    ys = arr[:,1].astype(int)
#    vals = arr[:,2]
#
#    # Determine grid size
#    # (max index +1 to include zero-based)
#    nx = xs.max() + 1
#    ny = ys.max() + 1
#
#    # Create an empty grid, fill with e.g. nan for missing data
#    grid = np.full((ny, nx), np.nan)

    # Fill in values
    #for x, y, v in zip(xs, ys, vals):
    #    grid[y, x] = v
#
#    fig, ax = plt.subplots()
#    ax.set_axis_off()
#    ax.set_box_aspect(1)
#    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
#    ax.imshow(grid, origin='lower', cmap='Greens', interpolation='none')
#    plt.savefig(f"output/{out}_density.png", bbox_inches='tight')
