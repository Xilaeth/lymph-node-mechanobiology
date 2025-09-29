import os
import sys

inp = sys.argv[1]
T = 15000
dt = 0.05
a = 1.0
a2 = 1.0
rm = 1.0
D = 0.01
en = T
f = 0.003
n = int(sys.argv[2])

for i in range(n):
    print(f"{i+1} of {n}")
    path = f"out_{i}"
    os.system(f"python3 ./run_param_load_force.py {inp} -T={T} -dt={dt} -a={a} -rm={rm} -D={D} -en={en} -fxr={f} -a2={a2}")
    os.system(f"mv ./output/out_1.vtk ./out/{path}.vtk")
    os.system(f"rm output/*")
os.sysatem(f"python3 average_vtk.py {n}")
