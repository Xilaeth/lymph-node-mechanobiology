import os
import sys

dt = 0.05
a = 1.0 
rmax = 1.0
T = int(sys.argv[2])
tot_saves = 1
var = 0
load = sys.argv[1]
D = 0.0
en = 150
tot_num = int(sys.argv[3])
name = sys.argv[4]
n = sys.argv[5]
f = float(sys.argv[6])

os.system(f"mkdir ./out/{name}-{n}-{f}")
os.system(f"mkdir ./out/{name}-{n}-{f}/saves")
os.system(f"cp load ./out/{name}-{n}-{f}/saves/init.vtk")

for N in range(tot_num):
    file = f"{name}_n-{n}_T-{T}_dt-{dt}_en-{en}_a-{a}_rm-{rmax}_D-{D}_f-{f}-{N}"
    os.system(f"python3 run_param_load.py {load} -a={a} -rm={rmax} -T={T} -dt={dt} -en={en} -D={D} -fxr={f}")
    os.system(f"zip -r -qq {file}.zip output")
    os.system(f"python3 v_anim.py ./output/out_ 100")
    os.system(f"mv 0.png ./out/{name}-{n}-{f}/init.png")
#    os.system(f"mv 1.png ./out/{name}-{n}-{f}/{file}.png")
    os.system(f"mv ./output/out_100.vtk ./out/{name}-{n}-{f}/saves/save-{N}.vtk")
    os.system(f"mv ./{file}.zip ./out/{name}-{n}-{f}/")
    os.system(f"rm ./output/*")
os.system(f"python3 average_vtk.py ./out/{name}-{n}-{f}/saves/save {tot_num} ./out/{name}-{n}-{f}/average")
os.system(f"python3 v.py ./out/{name}-{n}-{f}/average")
os.system(f"mv 0.png ./out/{name}-{n}-{f}/average.png")
