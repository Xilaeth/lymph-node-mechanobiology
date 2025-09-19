import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from math import floor

# read the file and split it by lines -> remove the first 6 lines
file = open("vtks/load_0.vtk", "rt")
content = file.read()
lines = content.splitlines()
lines = lines[6:]

# we create a list of the type [[x1, y1], [x2, y2],...]
coords = list(map(lambda x: list(map(lambda y: float(y), x.split(' ')))[:2], lines))

# isolate the x and y coordinates for ease of use
xs = list(map(lambda x: x[0], coords))
ys = list(map(lambda x: x[1], coords))

# function to check if a given coordinate v is in a square of side length l centered at x
def isInSquare(x, l, v):
    if ((abs(v[0] - x[0]) < l/2) and (abs(v[1] - x[1]) < l/2)):
        return True
    return False

# function that calculates the density of cells in a square of side length l centered at x
def densityInSquare(x, l):
    counter = 0
    for i in range(len(xs)):
        if (isInSquare(x, l, coords[i])):
            counter += 1
    return (counter / (l*l))

inp = 'lines'

# reads an image file as input
im = Image.open("pngs\\" + inp + ".png", 'r')
width, height = im.size
pixel_values = list(im.getdata())

# change the shape of the pixel values to [[r, g, b, alpha],...]
pixel_values = np.array(pixel_values).reshape((width, height, 4))

coordsOut = []

# define side length of the square we overlay the image over
l = 82 * 0.9
# set the center of the square
x = [44.5, 38.5]

for v in coords:
    if (not(isInSquare(x, l, v))):
        coordsOut.append(v)
        continue
    # the plus l/2 is to make sure (0, 0) is at the correct spot
    px = floor((v[0] + (l/2 - x[0]))*500/l)
    py = floor((v[1] + (l/2 - x[1]))*500/l)
    if (pixel_values[px][py][0] == 0):
        coordsOut.append(v)


xs = list(map(lambda x: x[0], coordsOut))
ys = list(map(lambda x: x[1], coordsOut))

leng = len(xs)

out = inp + "_out"

#with open(out + ".vtk", "w", encoding="ascii") as f:
#    f.write("# vtk DataFile Version 3.0\n")
#    f.write(out + "\n")
#    f.write("ASCII\n")
#    f.write("DATASET POLYDATA\n\n")
#    f.write("POINTS " + str(leng) + " float\n")
#    for i in coordsOut:
#        f.write(str(i[0]) + " " + str(i[1]) + " " + "0.0\n")

fig, ax = plt.subplots()
#ax.set_xlim([0, 2*x[0]])
#ax.set_ylim([0, 2*x[0]])

# Remove axes completely
#ax.set_axis_off()
#ax.set_box_aspect(1)

# Adjust figure so no padding remains
#plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
ax.scatter(xs, ys, s=0.05, c='red')


plt.show()
