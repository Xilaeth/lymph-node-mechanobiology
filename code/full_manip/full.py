import sys
import numpy as np
import tifffile

file = sys.argv[1]

#pages = tifffile.TiffFile(file).pages
#tarray = tifffile.TiffFile(file).asarray()

with tifffile.TiffFile(file) as tif:
    print(tif.is_imagej)
    print(tif.imagej_metadata)
