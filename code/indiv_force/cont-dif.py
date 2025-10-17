import os
import sys

a = 1.0
rm = 0.5
D = 0.0
dt = 0.05
T = 10
en = 10
file = sys.argv[1]
N = int(sys.argv[2])
f = float(sys.argv[3])
#dirs = [1, -2, -1, 2] # x, -y, -x, y
dirs = [1]
count = 0

for d in dirs:
    count += 1
#    os.system(f"mkdir ./out/dir-{d}")
    for i in range(N):
        print(f"{count}/{len(dirs)} - {i}/{N}")
        name = f"inp-{file}_T-{T}_dt-{dt}_a-{a}_rm-{rm}_D-{D}_N-{N}_f-{f}_id-{i}"
#        os.system(f"mkdir ./out/dir-{d}/{name}")
#        os.system(f"mv ./output/out-{i}_0.vtk ./out/dir-{d}/{name}/init.vtk")
#        os.system(f"mv ./output/out-{i}_1.vtk ./out/dir-{d}/{name}/end.vtk")
        s = os.popen(f"python3 dif.py -f1=./out/dir-{d}/{name}/init.vtk -f2=./out/dir-{d}/{name}/end.vtk -n={i}").read()
        os.system(f"echo \"{i} {s}\" >> ./out/dir-{d}/difs.txt")
