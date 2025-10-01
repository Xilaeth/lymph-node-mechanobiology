import os
import sys

dt = 0.05
a = 1.0 
rmax = 1.0
T = float(sys.argv[2])
tot_saves = 1
load = sys.argv[1]
D = 0.01
tot_num = int(sys.argv[3])
name = sys.argv[4]
n = sys.argv[5]
en = 150

os.system(f"mkdir ./out/{name}-{n}")
os.system(f"mkdir ./out/{name}-{n}/saves")
os.system(f"cp load ./out/{name}-{n}/saves/init.vtk")

for N in range(tot_num):
    file = f"{name}_n-{n}_T-{T}_dt-{dt}_en-{en}_a-{a}_rm-{rmax}_D-{D}-{N}"
    os.system(f"python3 run_param_load.py {load} -a={a} -rm={rmax} -T={T} -dt={dt} -en={en} -D={D}")
    os.system(f"zip -r -qq {file}.zip output")
    os.system(f"python3 v_anim.py ./output/out_ 100")
    os.system(f"mv 0.png ./out/{name}-{n}/init.png")
    os.system(f"mv 1.png ./out/{name}-{n}/{file}.png")
    os.system(f"mv ./output/out_100.vtk ./out/{name}-{n}/saves/save-{N}.vtk")
    os.system(f"mv ./{file}.zip ./out/{name}-{n}/")
    os.system(f"rm ./output/*")
os.system(f"python3 average_vtk.py ./out/{name}-{n}/saves/save {tot_num} ./out/{name}-{n}/average")
os.system(f"python3 v.py ./out/{name}-{n}/average")
os.system(f"mv 0.png ./out/{name}-{n}/average.png")
