import os
import sys

al = [0.2]
D = 0.0
dt = 0.01
T = 5000
en = int(T/100)
file = sys.argv[1]
frac = 1.0
n = len(al)
c = 0

for a in al:
    c += 1
    print(f"{c}/{n}")
    name = f"inp-{file}_T-{T}_dt-{dt}_a-{a}_D-{D}"
    os.system(f"mkdir ./out/{name}")
    os.system(f"python3 run-param-track.py {file}.vtk -a={a} -T={T} -D={D} -dt={dt} -en={en} -fr={frac}")
    os.system(f"mv ./output/* ./out/{name}")
