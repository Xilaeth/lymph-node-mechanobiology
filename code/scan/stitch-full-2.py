import os
import sys
import numpy as np

f1 = 0.95
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

folders = os.listdir("./out/")
#folders = os.listdir("./out/")
# wt - ht - w - h - x - y - fr - T - dt - a - b - rm - D - N - f
values = [get_list(i[4:]) for i in folders]

nx = values[0][2][1]
ny = values[0][3][1]
ht = values[0][0][1]

li = f1*ny*0.25*0.5*0.8659
lx = int(f1*f2*nx)

x = 0.5*(nx*0.25*0.5 - li)
y = 0.5*(ny*0.25*0.5*0.8659 - li)

mx = x
my = y

dif_tot = []
coords_tot = []
data_tot = []

# loop over all the parts
for i in range(len(values)):
    # top left corner in pixels
    cx0 = values[i][4][1]
    cy0 = values[i][5][1]
    # get top left in coords
    xc = ((cx0)/nx) * li
    yc = (((ht-1) - (cy0 + ny))/ny) * li
#    print(f"xc: {xc} - nx_c: {cx0}")
#    print(f"yc: {yc} - ny_c: {cy0}")
    # getting the vtk data
    file = open(f"./out/inp-wt-{int(values[i][0][1])}_ht-{int(values[i][1][1])}_w-{int(values[i][2][1])}_h-{int(values[i][3][1])}_x-{int(values[i][4][1])}_y-{int(values[i][5][1])}_f-{values[i][6][1]}_T-{int(values[i][7][1])}_dt-{values[i][8][1]}_a-{values[i][9][1]}_b-{values[i][10][1]}_D-{values[i][11][1]}_N-{int(values[i][12][1])}_f-{values[i][13][1]}/out_0.vtk", "rt")
    file2 = open(f"./out/inp-wt-{int(values[i][0][1])}_ht-{int(values[i][1][1])}_w-{int(values[i][2][1])}_h-{int(values[i][3][1])}_x-{int(values[i][4][1])}_y-{int(values[i][5][1])}_f-{values[i][6][1]}_T-{int(values[i][7][1])}_dt-{values[i][8][1]}_a-{values[i][9][1]}_b-{values[i][10][1]}_D-{values[i][11][1]}_N-{int(values[i][12][1])}_f-{values[i][13][1]}/data.csv", "rt")
    content = file.read()
    content2 = file2.read()
    lines = content.splitlines()
    lines = lines[6:]
    lines2 = content2.splitlines()

    coords = []
    fo = []

    sc = 0
    l = 0
    shift = 6
    # extract the coordinates from a given vtk file
    for j in lines:
        if (not(j) or (sc>0 and sc<(l+shift))):
            if (sc == (l+shift)):
                break
            sc += 1
        elif (sc == 0):
            tix, tiy, tiz = list(map(float, j.split(' ')))
            coords.append([tix, tiy, tiz])
            l += 1
        elif (sc > 0):
            if (j[0] == 'S'):
                break
            fo.append(j) 

    # make integers out of the type of cell
    #print(fo)
    fo = list(map(float, fo))

    # go over all the cells and check if they are inside 
    for j in range(len(coords)):
        if (fo[j] < 950):
            tix, tiy, tiz = coords[j]
            if ((np.abs(tix - (mx + li/2)) < f2*0.5*li) and (np.abs(tiy - (my + li/2)) < f2*0.5*li)):
                tx, ty, tz = coords[j]
                tx += xc
                ty += yc
                dx, dy, dz = list(map(float, lines2[j].split(',')))
                coords_tot.append([tx, ty, tz])
                data_tot.append([dx, dy, dz])
        else:
            continue

with open(f"stitch.vtk", "w", encoding="ascii") as f:
    f.write("# vtk DataFile Version 3.0\n")
    f.write("stitch" + "\n")
    f.write("ASCII\n")
    f.write("DATASET POLYDATA\n\n")
    f.write("POINTS " + str(len(coords_tot)) + " float\n")
    for i in coords_tot:
        f.write(str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + "\n")

with open(f"stitch.csv", "w", encoding="ascii") as f:
    for i in data_tot:
        f.write(str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + "\n")
