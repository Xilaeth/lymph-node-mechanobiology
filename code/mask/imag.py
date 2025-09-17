import numpy as np
from PIL import Image

im = Image.open('hole.png', 'r')
width, height = im.size
pixel_values = list(im.getdata())

print(pixel_values)

pixel_values = np.array(pixel_values).reshape((width, height, 4))

# implement a way of using the x and y values of a cell to figure out their pixel 
# we will add l to each coordinate to make it easier 
def getValue(x, y)

print(pixel_values[0][0])
