import os
import sys

files = []

for inp in sys.argv[1:]:
    files.append(inp)

al = [0.2] 
a2l = [0.1]
bl = [1.5]
req = 1.0
d = 2.0
Ds = [0.0, 0.01] 
dt = 0.05
T = 20000
en = int(T/100)
n = len(al)*len(bl)*len(Ds)*len(files)*len(a2l)
c = 0

for file in files:
    for a in al:
        for a2 in a2l:
            for b in bl:
                for D in Ds:
                    c += 1
                    print(f"{c}/{n}")
                    name = f"inp-{file}_T-{T}_dt-{dt}_a-{a}_b-{b}_req-{req}_d-{d}_D-{D}_a2-{a2}_beads"
                    os.system(f"mkdir ./out/{name}")
                    os.system(f"python3 run-param-track-beads.py {file}.vtk -a={a} -b={b} -d={d} -req={req} -T={T} -D={D} -dt={dt} -en={en} -a2={a2}")
                    os.system(f"mv ./output/* ./out/{name}")
