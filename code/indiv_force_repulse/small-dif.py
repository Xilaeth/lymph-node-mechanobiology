import os
import sys
import numpy as np
import tifffiles

file = 'input.tif'
a = ":)"

for inp in sys.argv[1:]:
    if (inp[0] == '-'):
        match inp[1:3]:
            case "a=":
                a = inp[3:]
                continue
    else:
        file = inp

coords_tot = []

tarray = tifffile.TiffFile(file).asarray()
