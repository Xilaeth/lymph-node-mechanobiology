import os
import sys

al = [0.2]
D = 0.0
dt = 0.01
T = 20000
en = int(T/100)
file = sys.argv[1]
frac = 1.5
n = len(al)
c = 0

force = float(sys.argv[2])
N = float(os.popen(f"python3 count.py {file}.vtk").read())
f *= float(1/N)

for a in al:
    c += 1
    print(f"{c}/{n}")
    name = f"inp-{file}_T-{T}_dt-{dt}_a-{a}_D-{D}_f-{force}_N-{N}"
    os.system(f"mkdir ./out/{name}")
    os.system(f"python3 run-param-track.py {file}.vtk -a={a} -T={T} -D={D} -dt={dt} -en={en} -fr={frac} -fo={force}")
    os.system(f"mv ./output/* ./out/{name}")
