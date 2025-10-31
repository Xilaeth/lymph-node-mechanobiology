import os
import sys

a = 1.0
rm = 2.0
D = 0.0
dt = 0.05
T = 5
#en = int(T/100)
en = 1
file = sys.argv[1]
f = float(sys.argv[2])
fid = int(sys.argv[3])
F = 2.0
F1 = 0.1
a1 = 1.0
#dirs = [1, -2, -1, 2] # x, -y, -x, y
dirs = [1]

N = int(os.popen(f"python3 count.py {file}.vtk").read())
print(N)

for d in dirs:
#    os.system(f"mkdir ./out/dir-{d}")
#    os.system(f"touch ./out/dir-{d}/difs.txt")
    os.system(f"python3 run_param_load_single.py {file}.vtk -a={a} -rm={rm} -T={T} -D={D} -f={f} -dt={dt} -en={en} -fdir={d} -nr={N} -F={F} -fi={fid} -F1={F1} -a1={a1}")
#    for i in range(N):
#        if (not(i == 0)):
#            continue
#        print(f"{i}/{N}")
#        name = f"inp-{file}_T-{T}_dt-{dt}_a-{a}_rm-{rm}_D-{D}_N-{N}_f-{f}_id-{i}"
#        os.system(f"mkdir ./out/dir-{d}/{name}")
#        os.system(f"mv ./output/out-{i}_* ./out/dir-{d}/{name}")
#        os.system(f"mv ./output/out-{i}_0.vtk ./out/dir-{d}/{name}/init.vtk")
#        os.system(f"mv ./output/out-{i}_1.vtk ./out/dir-{d}/{name}/end.vtk")
        #s = os.popen(f"python3 dif.py -f1=./out/dir-{d}/{name}/init.vtk -f2=./out/dir-{d}/{name}/end.vtk -n={i}").read()
        #os.system(f"echo \"{i} {s}\" >> ./out/dir-{d}/difs.txt")
