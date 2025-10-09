import os
import sys

a = 1.0
rm = 1.0
D = 0.0
dt = 0.05
T = 10
en = 10
file = sys.argv[1]
N = int(sys.argv[2])
f = float(sys.argv[3])
dirs = [1, -2, -1, 2] # x, -y, -x, y

for i in range(N):
    for d in dirs:
        name = f"inp-{file}_T-{T}_dt-{dt}_a-{a}_rm-{rm}_D-{D}_N-{N}_f-{f}_dir-{d}"
        os.system(f"mkdir ./out/{name}")
        os.system(f"mkdir ./out/{name}")
        os.system(f"python3 run_param_load.py -a={a} -rm={rm} -T={T} -D={D} -f={f} -dt={dt} -en={en} -fid={i} -fdir={d}")
        os.system(f"mv ./output/out_0.vtk ./out/{name}/init.vtk")
        os.system(f"mv ./output/out_1.vtk ./out/{name}/end.vtk")
