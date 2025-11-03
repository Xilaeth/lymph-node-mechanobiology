import os
import sys

f1 = 1.0
f2 = 0.95

def get_list(s):
    s += '_'
    mode = 0
    out_n = []
    out_v = []
    cur = ''
    for c in s:
        match mode:
            case 0:
                if (c == '-'):
                    out_n.append(cur)
                    cur = ''
                    mode = 1
                    continue
                else:
                    cur += c
            case 1:
                if (c == '_'):
                    out_v.append(cur)
                    cur = ''
                    mode = 0
                    continue
                else:
                    cur += c
    l = len(out_n)
    return [[out_n[i], float(out_v[i])] for i in range(l)]

folders = os.listdir("./out-vtk")
#folders = os.listdir("./out/")
# wt - ht - w - h - x - y - fr - T - dt - a - rm - D - N - f
values = [get_list(i[:-4]) for i in folders]

x = ((1-f1*f2)/2)*nx*0.5
y = ((1-f1*f2)/2)*ny*0.5*0.8660
lx = f1*f2*0.5*nx
ly = f1*f2*0.5*ny*0.8660

# pairs of points and displacements [points, displace]
pairs = []
coords_tot = []

# loop over all the parts
for i in range(len(values)):
    # top left corner in pixels
    cx0 = values[i][4][1]
    cy0 = values[i][5][1]
    # get top left in coords
    xc = fx*cx0
    yc = (1999 - (cy0 + ny))*fy 
    # getting the vtk data
    file = open(f"./out-vtk/wt-{int(values[i][0][1])}_ht-{int(values[i][1][1])}_w-{int(values[i][2][1])}_h-{int(values[i][3][1])}_x-{int(values[i][4][1])}_y-{int(values[i][5][1])}_f-{values[i][6][1]}.vtk", "rt")
    content = file.read()
    lines = content.splitlines()
    lines = lines[6:]

    coords = []
    fo = []

    sc = 0
    for j in lines:
        if (not(j) or (sc>0 and sc<4)):
            if (sc == 4):
                break
            sc += 1
        elif (sc == 0):
            tix, tiy, tiz = list(map(float, j.split(' ')))
            tix += xc
            tiy += yc
            coords.append([tix, tiy, tiz])
        elif (sc > 0):
            fo.append(j)   
    fo = list(map(int, fo))
    for j in range(len(coords)):
        if (fo[j] == 1):
            coords_tot.append(coords[j])
        else:
            continue
