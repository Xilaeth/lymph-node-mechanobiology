import os
import sys

a = 0.2
b = 0.01
D = 0.0
dt = 0.01
T = 5000
en = int(T/100)
file = sys.argv[1]
frac = 1.0

force = float(sys.argv[2])
N = float(os.popen(f"python3 count.py {file}.vtk").read())
force *= float(1/N)

name = f"inp-{file}_T-{T}_dt-{dt}_a-{a}_b-{b}_D-{D}_f-{force}_N-{N}"
os.system(f"mkdir ./out/{name}")
os.system(f"python3 run-param-track-beads.py {file}.vtk -a={a} -T={T} -D={D} -dt={dt} -en={en} -fr={frac} -b={b} -fo={force}")
os.system(f"mv ./output/* ./out/{name}")
