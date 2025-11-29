import os
import sys

al = [0.2]
D = 0.0
dt = 0.2
T = 5
#en = int(T/100)
en = T
file = sys.argv[1]
f = float(sys.argv[2])
bl = [0.01]
#dirs = [1, -2, -1, 2] # x, -y, -x, y
dirs = [1]
frs = [0.5, 1.0, 1.5, 2.0]

N = int(os.popen(f"python3 count.py {file}.vtk").read())
print(N)
n = len(dirs)*len(al)*len(bl)*len(frs)
c = 0

for d in dirs:
    for a in al:
        for b in bl:
            for fr in frs:
                c += 1
                print(f"{c}/{n}")
                name = f"inp-{file}_T-{T}_dt-{dt}_a-{a}_b-{b}_D-{D}_N-{N}_f-{f}_fr-{fr}"
                os.system(f"mkdir ./out/{name}")
                os.system(f"python3 run_param_small.py {file}.vtk -a={a} -T={T} -D={D} -f={f} -dt={dt} -en={en} -fdir={d} -nr={N} -b={b}")
                os.system(f"mv ./output/out_0.vtk ./out/{name}")
                os.system(f"python3 small-dif.py ./out/{name}/out_0.vtk")
                os.system(f"mv ./data.csv ./out/{name}")
