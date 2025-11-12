import os
import sys

a = 0.2
D = 0.0
dt = 0.05
T = 10
#en = int(T/100)
en = T
file = sys.argv[1]
f = float(sys.argv[2])
b = 0.01
#dirs = [1, -2, -1, 2] # x, -y, -x, y
dirs = [1]

N = int(os.popen(f"python3 count.py {file}.vtk").read())
print(N)

for d in dirs:
    name = f"inp-{file}_T-{T}_dt-{dt}_a-{a}_b-{b}_D-{D}_N-{N}_f-{f}"
    os.system(f"mkdir ./out/{name}")
    os.system(f"python3 run_param_small.py {file}.vtk -a={a} -T={T} -D={D} -f={f} -dt={dt} -en={en} -fdir={d} -nr={N} -b={b}")
    os.system(f"mv ./output/out_0.vtk ./out/{name}")
    os.system(f"python3 small-dif.py ./out/{name}/out_0.vtk")
    os.system(f"mv ./data.csv ./out/{name}")
