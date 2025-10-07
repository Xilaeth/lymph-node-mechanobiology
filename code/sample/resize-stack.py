import os
import sys
import numpy
from tifffile import imread, imwrite

x = 100
name = "inp.tif"

for inp in sys.argv[1:]:
    if (inp[0] == "-"):
        match inp[1:3]:
            case "x=":
                x = int(inp[3:])
                continue
    else:
        name = inp

im_data = imread(name)
d, h, w = im_data.shape
new = []

for z in range(d):
    temp = im_data[z, :, :]
    imwrite(f"out.tif", temp, photometric='minisblack', dtype='uint8')
    os.system(f"ffmpeg -loglevel error -hide_banner -i out.tif -vf scale={x}:-1 out2.tif")
    temp2 = imread(f"out2.tif")
    new.append(temp2)
    os.system("rm out*.tif")

imwrite('out.tif', new, photometric='minisblack', dtype='uint8')

