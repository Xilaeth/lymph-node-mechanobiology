import os
import sys

dt = 0.1
a = 1.0 
rmax = 1.0
T = float(sys.argv[2])
tot_saves = 1
var = 0
load = sys.argv[1]
D = 0.01
tot_num = int(sys.argv[3])
f = 0.01

for n in range(tot_num):
    every_n = int(int(T/dt) / tot_saves)
    file = f"0-{T}_a-{a}_rmax-{rmax}_D-{D}"
    os.system(f"python3 run_param_load.py {load} -a={a} -rm={rmax} -T={int(T/dt)} -dt={dt} -en={every_n} -D={D} -f={f}")
    os.system(f"python3 read-all.py ./output/out_ {tot_saves} ./forces")
    os.system(f"rm ./output/*")
    os.system(f"cp ./forces/positions{tot_saves}.vtk ./")
    os.system(f"mv ./positions{tot_saves}.vtk ./out/{file}-{n}.vtk")
    os.system(f"rm ./forces/*")
os.system(f"python3 average_vtk.py 0-{T}_a-{a}_rmax-{rmax}_D-{D} {tot_num} average")
