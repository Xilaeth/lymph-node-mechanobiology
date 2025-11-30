import os
import sys

a = 0.2
b = 0.01
D = 0.0
dt = 0.01
T = 1000
en = int(T/100)
file = sys.argv[1]
frac = 1.0
N = int(os.popen(f"python3 count.py {file}.vtk").read())

name = f"inp-{file}_T-{T}_dt-{dt}_a-{a}_b-{b}_D-{D}"
os.system(f"mkdir ./out/{name}")
os.system(f"python3 run-param-track-beads.py {file}.vtk -a={a} -T={T} -D={D} -dt={dt} -en={en} -fr={frac} -b={b} -nr={N}")
os.system(f"mv ./output/* ./out/{name}")
