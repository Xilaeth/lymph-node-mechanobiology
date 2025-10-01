import os 
import sys

n_list = [10000, 40000, 90000]
a_list = [0.5, 1.0, 2.5]
rm_list = [0.5, 1.0 ,2.5]
name_list = ["lines", "small_lines"]
T = 15000
dt = 0.05
en = 150
D = 0.0

for name in name_list:
    os.system(f"mkdir ./out/{name}")
    for n in n_list:
        for a in a_list:
            for rm_ in rm_list:
                fold = f"{name}_n-{n}_T-{T}_dt-{dt}_en-{en}_a-{a}_rm-{rm}"
                os.system(f"python3 run_param_load.py ./out_{name}_n{n}.vtk -a={a} -rm={rm} -T={T} -dt={dt} -D={D} -f=0.0 -en={en}")
                os.system(f"zip -r -qq {fold}.zip ./output")
                os.system(f"python3 v_anim.py ./output/out_ 100")
                os.system(f"mv {folder}.zip ./out/{name}/")
                os.system(f"mv ./0.png ./out/{name}/{name}_n-{n}_init.png")
                os.system(f"mv ./1.png ./out/{name}/{fold}.png")
                os.system(f"rm output/*")
