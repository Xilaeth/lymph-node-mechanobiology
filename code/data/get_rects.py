import sys
import numpy as np
import tifffile

file = sys.argv[1]

data = tifffile.TiffFile(file).asarray()

print(data)
