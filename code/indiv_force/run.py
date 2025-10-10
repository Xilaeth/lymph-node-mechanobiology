import os
import sys

a = 1.0
rm = 1.0
D = 0.0
dt = 0.05
T = 100
en = T
file = sys.argv[1]
N = int(sys.argv[2])
f = float(sys.argv[3])
#dirs = [1, -2, -1, 2] # x, -y, -x, y
dirs = [2]

for d in dirs:
    os.system(f"mkdir ./out/dir-{d}")
    os.system(f"touch ./out/dir-{d}/difs.txt")
    for i in range(N):
        name = f"inp-{file}_T-{T}_dt-{dt}_a-{a}_rm-{rm}_D-{D}_N-{N}_f-{f}_id-{i}"
        os.system(f"mkdir ./out/dir-{d}/{name}")
        os.system(f"python3 run_param_load.py {file}.vtk -a={a} -rm={rm} -T={T} -D={D} -f={f} -dt={dt} -en={en} -fid={i} -fdir={d}")
        os.system(f"mv ./output/out_0.vtk ./out/dir-{d}/{name}/init.vtk")
        os.system(f"mv ./output/out_1.vtk ./out/dir-{d}/{name}/end.vtk")
        s = os.popen(f"python3 dif.py -f1=./out/dir-{d}/{name}/init.vtk -f2=./out/dir-{d}/{name}/end.vtk -n={i}").read()
        os.system(f"echo \"{i} {s}\" >> ./out/dir-{d}/difs.txt")
