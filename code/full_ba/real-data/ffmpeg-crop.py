import os
import sys

file = "input.tif"
x = 0
y = 0
w = 0
h = 0

for inp in sys.argv[1:]:
    if (inp[0] == '-'):
        match inp[1:3]:
            case "x=":
                x = inp[3:]
                continue
            case "y=":
                y = inp[3:]
                continue
            case "w=":
                w = inp[3:]
                continue
            case "h=":
                h = inp[3:]
                continue
    else:
        file = inp

os.system(f'ffmpeg -i {file} -vf "crop={w}:{h}:{x}:{y}" output.tif')
