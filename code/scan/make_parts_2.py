import sys
import os
from math import floor

file = "input.tif"
w = 0
h = 0
wtot = 0
htot = 0
f = 0.05

for inp in sys.argv[1:]:
    if (inp[0] == '-'):
        match inp[1:3]:
            case "w=":
                w = int(inp[3:])
                continue
            case "h=":
                h = int(inp[3:])
                continue
            case "f=":
                f = float(inp[3:])
                continue
        match inp[1:4]:
            case "wt=":
                wtot = int(inp[4:])
                continue
            case "ht=":
                htot = int(inp[4:])
                continue
    else:
        file = inp

lh = (1-f)*(1-f)*h
lw = (1-f)*(1-f)*w
nw = 1 + (floor(wtot / lw))
nh = 1 + (floor(htot / lh))

nt = nw*nh

cx = 0
cy = 0
count = 0

for i in range(nw):
    if (i == 0):
        cx = 0
    elif (i == (nw-1)):
        cx = int(wtot - w)
    else:
        cx += int(lw)
    for j in range(nh):
        count += 1
        print(f"{count}/{nt}")
        if (j == 0):
            cy = 0
        elif (j == (nh-1)):
            cy = int(htot - h)
        else:
            cy += int(lh)

        os.system(f"python3 ffmpeg-crop.py {file} -x={cx} -y={cy} -w={w} -h={h}")
        os.system(f"mv output.tif ./out-tif/wt-{wtot}_ht-{htot}_w-{w}_h-{h}_x-{cx}_y-{cy}_f-{f}.tif")

