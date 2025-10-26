import sys
import numpy as np
import matplotlib.pyplot as plt

load = 'data.csv'
x = 'x'
y = 'y'
mode = 0

index = [-1, -1, -1, -1, -1, -1]

for inp in sys.argv[1:]:
    if (inp[0] == '-'):
        match inp[1:3]:
            case "x=":
                x = inp[3:]
                continue
            case "y=":
                y = inp[3:]
                continue
            case "a=":
                index[2] = int(inp[3:])
                continue
            case "F=":
                index[4] = int(inp[3:])
                continue
            case "f=":
                index[5] = int(inp[3:])
                continue
            case "m=":
                mode = int(inp[3:])
                continue
        match inp[1:4]:
            case "nx=":
                index[0] = int(inp[4:])
                continue
            case "ny=":
                index[1] = int(inp[4:])
                continue
            case "rm=":
                index[3] = int(inp[4:])
                continue
    else:
        load = inp

match x:
    case "nx":
        xi = 0
    case "ny":
        xi = 1
    case "a":
        xi = 2
    case "rm":
        xi = 3
    case "F":
        xi = 4
    case "f":
        xi = 5
    case "q":
        xi = 9

match y:
    case "nx":
        yi = 0
    case "ny":
        yi = 1
    case "a":
        yi = 2
    case "rm":
        yi = 3
    case "F":
        yi = 4
    case "f":
        yi = 5
    case "q":
        yi = 9

data = np.loadtxt(load, delimiter=',')

nxs = np.sort(np.unique(data[:, 0]))
nys = np.sort(np.unique(data[:, 1]))
ass = np.sort(np.unique(data[:, 2]))
rms = np.sort(np.unique(data[:, 3]))
Fs = np.sort(np.unique(data[:, 4]))
fs = np.sort(np.unique(data[:, 5]))

look_up = [nxs, nys, ass, rms, Fs, fs]

m1_val = -1

for i in range(6):
    if (index[i] == -1):
        if (not(i == xi or i == yi)):
            m1_val = i
        continue
    data = list(map(lambda x: (x if x[i] == look_up[i][index[i]] else []) if not(list(x) == []) else [] , data))

m1_val_name = 'x'

match m1_val:
    case 0:
        m1_val_name = 'nx'
    case 1:
        m1_val_name = 'ny'
    case 2:
        m1_val_name = 'a'
    case 3:
        m1_val_name = 'rm'
    case 4:
        m1_val_name = 'F'
    case 5:
        m1_val_name = 'f'

if (mode == 0):
    data_out = []

    for i in range(len(data)):
        if (list(data[i]) == []):
            continue
        if (data[i][xi] == -1 or data[i][yi] == -1):
            continue
        data_out.append(list(data[i]))

    data = np.array(data_out)

    plt.scatter(data[:, xi], data[:, yi], s=5, c='black')
elif (mode == 1):
    data_out = []

    for j in look_up[m1_val]:
        data_temp = []
        for i in range(len(data)):
            if (list(data[i]) == []):
                continue
            if (data[i][xi] == -1 or data[i][yi] == -1):
                continue
            if (not(data[i][m1_val] == j)):
                continue
            data_temp.append(list(data[i]))
        data_out.append(np.array(data_temp))
         
    for j in range(len(look_up[m1_val])):
        plt.scatter(data_out[j][:, xi], data_out[j][:, yi], s=5, label=f"{m1_val_name}: {look_up[m1_val][j]}")

    plt.legend()

plt.xlabel(f"{x}")
plt.ylabel(f"{y}")
plt.show()
