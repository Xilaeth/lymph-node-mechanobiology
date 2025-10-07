import os 
import sys

n_list = [10000, 40000]
a_list = [1.0]
rm_list = [1.0]
name_list = ["lines", "small_lines"]
f_list = [0.2, 0.4, 0.8]
T = 15000
dt = 0.05
en = 150
D = 0.0
tot_num = int(sys.argv[1])
tot = len(n_list)*len(a_list)*len(rm_list)*len(name_list)*len(f_list)

i = 0

for name in name_list:
    for n in n_list:
        for a in a_list:
            for rm in rm_list:
                for f in f_list:
                    i += 1
                    print(f"{i}/{tot}")
                    file = f"{name}_n-{n}_a-{a}_rm-{rm}_f-{f}"
                    os.system(f"mkdir ./out/{file}")
                    os.system(f"mkdir ./out/{file}/saves")
                    os.system(f"cp out_{name}_n{n}.vtk ./out/{file}/saves/init.vtk")
                    tn = int(os.popen(f"python3 get_num.py out_{name}_n{n}").read())
                    for N in range(tot_num):
                        fx = f/tn
                        cur = f"{name}_n-{n}_T-{T}_dt-{dt}_en-{en}_a-{a}_rm-{rm}_D-{D}_f-{f}-{N}"
                        os.system(f"python3 run_param_load_force.py out_{name}_n{n}.vtk -a={a} -rm={rm} -T={T} -dt={dt} -en={en} -D={D} -fxr={fx}")
                        os.system(f"zip -r -qq {cur}.zip output")
#                        os.system(f"python3 v_anim.py ./output/out_ 100")
#                        os.system(f"mv 0.png ./out/{file}/init.png")
                        os.system(f"mv ./output/out_100.vtk ./out/{file}/saves/save_end-{N}.vtk")
                        os.system(f"mv ./output/out_0.vtk ./out/{file}/saves/save_start-{N}.vtk")
                        os.system(f"mv ./{cur}.zip ./out/{file}/")
                        os.system(f"rm ./output/*")
#                    os.system(f"python3 average_vtk.py ./out/{file}/saves/save {tot_num} ./out/{file}/average")
#                    os.system(f"python3 v.py ./out/{file}/average")
#                    os.system(f"mv 0.png ./out/{file}/average.png")
