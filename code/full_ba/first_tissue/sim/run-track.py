import os
import sys

al = [0.1, 0.2, 0.4]
bl = [1.0, 1.5, 2.0]
req = 1.0
d = 2.0
D = 0.0
dt = 0.05
T = 2500
en = int(T/100)
file = sys.argv[1]
n = len(al)*len(bl)
c = 0

for a in al:
    for b in bl:
        c += 1
        print(f"{c}/{n}")
        name = f"inp-{file}_T-{T}_dt-{dt}_a-{a}_b-{b}_req-{req}_d-{d}"
        os.system(f"mkdir ./out/{name}")
        os.system(f"python3 run-param-track.py {file}.vtk -a={a} -b={b} -d={d} -req={req} -T={T} -D={D} -dt={dt} -en={en}")
        os.system(f"mv ./output/* ./out/{name}")
