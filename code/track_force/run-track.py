import os
import sys

al = [0.2]
D = 0.0
dt = 0.01
T = 100
en = int(T/100)
#en = T
file = sys.argv[1]
bl = [0.01]
#dirs = [1, -2, -1, 2] # x, -y, -x, y
dirs = [1]
frs = [1]

n = len(dirs)*len(al)*len(bl)*len(frs)
c = 0

for d in dirs:
    for a in al:
        for b in bl:
            for fr in frs:
                c += 1
                print(f"{c}/{n}")
                name = f"inp-{file}_T-{T}_dt-{dt}_a-{a}_b-{b}_D-{D}"
                os.system(f"mkdir ./out/{name}")
                os.system(f"python3 run-param-track.py {file}.vtk -a={a} -T={T} -D={D} -dt={dt} -en={en} -b={b}")
                os.system(f"mv ./output/* ./out/{name}")
