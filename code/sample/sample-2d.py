import sys
import numpy as np
from tifffile import imread, imwrite
from math import floor
from PIL import Image

x1 = 5
x2 = 10
y1 = 5
y2 = 10
name = "inp.vtk"

for inp in sys.argv[1:]:
    if (inp[0] == "-"):
        match inp[1:4]:
            case "x1=":
                x1 = int(inp[4:])
                continue
            case "x2=":
                x2 = int(inp[4:])
                continue
            case "y1=":
                y1 = int(inp[4:])
                continue
            case "y2=":
                y2 = int(inp[4:])
                continue
    else:
        name = inp

im_data = imread(name)
h, w = im_data.shape
coordsOut = np.zeros((y2-y1+1, x2-x1+1), dtype=np.uint8)

for x in range(0, x2-x1):
    for y in range(0, y2-y1):
        coordsOut[y2-y1-y][x] = im_data[h - (y1 + y)][x1 + x]*255

print(coordsOut)

imwrite('out.tif', coordsOut, photometric='minisblack', dtype='uint8')
