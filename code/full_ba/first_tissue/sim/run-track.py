import os
import sys

al = [0.2]
bl = [1.5, 2.0]
req = 1.0
d = 2.0
Ds = [0.00, 0.01, 0.02]
dt = 0.05
T = 10000
en = int(T/100)
#file = sys.argv[1]
files = ["nx-12_ny-12_l-09", "L-10_N-128", "nx-24_ny-24_l-11", "L-20_N-512"]
n = len(al)*len(bl)*len(Ds)*len(files)
c = 0

for file in files:
    for a in al:
        for b in bl:
            for D in Ds:
                c += 1
                print(f"{c}/{n}")
                name = f"inp-{file}_T-{T}_dt-{dt}_a-{a}_b-{b}_req-{req}_d-{d}_D-{D}"
                os.system(f"mkdir ./out/{name}")
                os.system(f"python3 run-param-track.py {file}.vtk -a={a} -b={b} -d={d} -req={req} -T={T} -D={D} -dt={dt} -en={en}")
                os.system(f"mv ./output/* ./out/{name}")
