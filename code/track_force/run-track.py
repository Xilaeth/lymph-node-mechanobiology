import os
import sys

al = [0.1, 0.2, 0.4]
D = 0.0
dt = 0.05
T = 1000
en = int(T/100)
#file = sys.argv[1]
files = ["68-68-no-edge", "125-125-no-edge"]
fracs = [1.0, 1.5, 2.0]
n = len(al)*len(fracs)
c = 0

for a in al:
    for frac in fracs:
        for file in files:
            c += 1
            print(f"{c}/{n}")
            name = f"inp-{file}_T-{T}_dt-{dt}_a-{a}_fr-{frac}"
            os.system(f"mkdir ./out/{name}")
            os.system(f"python3 run-param-track.py {file}.vtk -a={a} -T={T} -D={D} -dt={dt} -en={en} -fr={frac}")
            os.system(f"mv ./output/* ./out/{name}")
