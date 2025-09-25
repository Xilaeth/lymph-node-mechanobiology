from PIL import Image
import sys
import numpy as np

im = Image.open(sys.argv[1])
im_data = np.array(im)
print(im_data.shape)
print(im_data.size)
for i in range(im_data.shape[0]):
    for j in range(im_data.shape[1]):
        if im_data[i][j] == 1:
            im_data[i][j] = 255

print(im_data)
im_new = Image.fromarray(im_data)
im_new.save("out.tif")
