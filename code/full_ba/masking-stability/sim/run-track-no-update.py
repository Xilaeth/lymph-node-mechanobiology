import os
import sys

files = []

for inp in sys.argv[1:]:
    files.append(inp)

al = [0.2] 
bl = [1.5]
req = 1.0
d = 2.0
Ds = [0.0] 
dt = 0.05
T = 1000
en = T+2#int(T/100)
n = len(al)*len(bl)*len(Ds)*len(files)
c = 0

for file in files:
    for a in al:
        for b in bl:
            for D in Ds:
                c += 1
                print(f"{c}/{n}")
                name = f"inp-{file}_T-{T}_dt-{dt}_a-{a}_b-{b}_req-{req}_d-{d}_D-{D}_no-update"
                os.system(f"mkdir ./out/{name}")
                os.system(f"python3 run-param-track-no-update.py {file}.vtk -a={a} -b={b} -d={d} -req={req} -T={T} -D={D} -dt={dt} -en={en}")
                os.system(f"mv ./output/* ./out/{name}")
