import os
import sys

dt = 0.1
a = 1.0 
rmax = 1.0
T = int(sys.argv[2])
tot_saves = 1
var = 0
load = sys.argv[1]
D = 0.001
tot_num = int(sys.argv[3])

for n in range(tot_num):
    print(f"Starting: {n}")
    every_n = int(int(T/dt) / tot_saves)
    file = f"0-{T}_a-{a}_rmax-{rmax}_D-{D}"
    os.system(f"python3 run_param_load.py {load} -a={a} -rm={rmax} -T={T} -dt={dt} -en={every_n} -D={D}")
    os.system(f"python3 read-all.py ./output/out_ {tot_saves - 1} ./forces")
    os.system(f"rm ./output/*")
    os.system(f"cp ./forces/positions{tot_saves - 1}.vtk ./")
    os.system(f"mv ./positions{tot_saves - 1}.vtk ./out/{file}-{n}.vtk")
    os.system(f"rm ./forces/*")
