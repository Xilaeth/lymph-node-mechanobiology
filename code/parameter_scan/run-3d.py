import os 
import sys

n_list = [[120, 120, 15], [190, 190, 24], [250, 250, 31]]
a_list = [0.5]#, 1.0, 2.5]
rm_list = [0.5]#, 0.6, 0.7]
name_list = ["P6059"]
#f_list = [0.2, 0.4, 0.8]
T = 2000
dt = 0.05
en = 20
D = 0.0
tot_num = int(sys.argv[1])
tot = len(n_list)*len(a_list)*len(rm_list)*len(name_list)#*len(f_list)
fx = 0
i = 0

for name in name_list:
    for n in n_list:
        for a in a_list:
            for rm in rm_list:
                i += 1
                print(f"{i}/{tot}")
                file = f"{name}_nx-{n[0]}_ny-{n[1]}_nz-{n[2]}_a-{a}_rm-{rm}_T-{T}_dt-{dt}_en-{en}_D-{D}"
                os.system(f"mkdir ./out/{file}")
                os.system(f"mkdir ./out/{file}/saves")
                #tn = int(os.popen(f"python3 get_num.py {name}_nx-{n[0]}_ny-{n[1]}_nz-{n[2]}").read())
                for N in range(tot_num):
 #                   fx = f/tn
                    cur = f"{name}_nx-{n[0]}_ny-{n[1]}_nz-{n[2]}_a-{a}_rm-{rm}_T-{T}_dt-{dt}_en-{en}_D-{D}_N-{N}"
                    os.system(f"python3 run_param_load_ord.py {name}_nx-{n[0]}_ny-{n[1]}_nz-{n[2]}.vtk -a={a} -rm={rm} -T={T} -dt={dt} -en={en} -D={D} -fxr={fx}")
                    os.system(f"zip -r {cur}.zip output")
                    os.system(f"mv ./output/out_100.vtk ./out/{file}/saves/save_end-{N}.vtk")
                    os.system(f"mv ./output/out_0.vtk ./out/{file}/saves/save_start-{N}.vtk")
#                    e1 = float(os.popen(f"python3 quant-stretch.py ./out/{file}/saves/save_start-{N}.vtk")).read()
#                    e2 = float(os.popen(f"python3 quant-stretch.py ./out/{file}/saves/save_end-{N}.vtk")).read()
#                    os.system(f"echo {e1} >> ./out/{file}/saves/ecc-{N}.txt")
#                    os.system(f"echo {e2} >> ./out/{file}/saves/ecc-{N}.txt")
                    os.system(f"mv ./{cur}.zip ./out/{file}/")
                    os.system(f"rm ./output/*")
