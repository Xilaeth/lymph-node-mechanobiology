import os
import sys

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
values = [get_list(i) for i in folders]

with open(f"./out/data.csv", "w", encoding="ascii") as f:
    for i in range(len(values)):
        print(f"{i}/{len(values)}")
        # nx - ny - a - rm - F - f - T - dt - m - quant-stretch
        q = float(os.popen(f"python3 dif.py {folders[i]}").read())
        f.write(f"{values[i][0][1]},{values[i][1][1]},{values[i][2][1]},{values[i][3][1]},{values[i][4][1]},{values[i][5][1]},{values[i][6][1]},{values[i][7][1]},{values[i][8][1]},{q}\n")
