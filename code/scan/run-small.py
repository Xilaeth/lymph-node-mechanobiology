import os
import sys

a = 1.0
rm = 2.0
D = 0.0
dt = 0.05
T = 1
#en = int(T/100)
en = T
file = sys.argv[1]
f = float(sys.argv[2])
F = 2.0
F1 = 0.1
a1 = 1.0
dirs = [1]

N = int(os.popen(f"python3 count.py {file}.vtk").read())
print(N)

for d in dirs:
    name = f"inp-{file}_T-{T}_dt-{dt}_a-{a}_rm-{rm}_D-{D}_N-{N}_f-{f}"
    os.system(f"mkdir ./out/{name}")
    os.system(f"python3 run_param_small.py {file}.vtk -a={a} -rm={rm} -T={T} -D={D} -f={f} -dt={dt} -en={en} -fdir={d} -nr={N} -F={F} -F1={F1} -a1={a1}")
    os.system(f"mv ./output/out_0.vtk ./out/{name}")
    os.system(f"python3 small-dif.py ./out/{name}/out_0.vtk")
    os.system(f"mv ./data.csv ./out/{name}")
