import os
import sys

dt_list = [0.01] #, 0.05, 0.1, 0.5, 1.0]
a_list = [1.0] #[0.2, 0.5, 1.0, 2.0, 5.0]
n_list = [100000] #[900, 1600, 2500, 10000, 40000]
rmax = 1.0
T = 0.1
tot_saves = 10
r_start = 0.5
var = 0
frac = 0.1
D = 0.01
ns = int(sys.argv[1])

for dt in dt_list:
    for a in a_list:
        for n in n_list:
            #i = 0
            #while (True):
            for i in range(ns):
                every_n = int(int(T/dt) / tot_saves)
                if (i == 0):
                    folder = f"0-{int(T/dt)}_dt-{dt}_a-{a}_n-{n}"
                    os.system(f"mkdir ./out/{folder}")
                    os.system(f"python3 run_param.py -n={n} -a={a} -rm={rmax} -T={int(T/dt)} -dt={dt} -en={every_n} -sd={r_start} -D={D}")
                    os.system(f"python3 read-all.py ./output/out_ {tot_saves} ./forces")
                    os.system(f"rm ./output/*")
                    os.system(f"python3 eval.py ./forces/forces {tot_saves} ./out/{folder}/convergence_0-{int(T/dt)}_dt-{dt}.png ./out/{folder}")
                    os.system(f"cp ./forces/positions{tot_saves}.vtk ./")
                    os.system(f"mv ./positions{tot_saves}.vtk ./load.vtk")
                    os.system(f"zip -r -qq {folder}.zip ./forces")
                    os.system(f"mv {folder}.zip ./out/{folder}")
                    os.system(f"rm ./forces/*")
                    var = float(os.popen(f"python3 eval2.py ./out/{folder}/forces.csv").read()) 
                else:
                    folder = f"{i*int(T/dt)}-{(i+1)*int(T/dt)}_dt-{dt}_a-{a}_n-{n}"
                    os.system(f"mkdir ./out/{folder}")
                    os.system(f"python3 run_param_load.py load.vtk -a={a} -rm={rmax} -T={int(T/dt)} -dt={dt} -en={every_n} -D={D}")
                    os.system(f"python3 read-all.py ./output/out_ {tot_saves} ./forces")
                    os.system(f"rm ./output/*")
                    os.system(f"python3 eval.py ./forces/forces {tot_saves} ./out/{folder}/convergence_{i*int(T/dt)}-{(i+1)*int(T/dt)}_dt-{dt}.png ./out/{folder}")
                    os.system(f"cp ./forces/positions{tot_saves}.vtk ./")
                    os.system(f"mv ./positions{tot_saves}.vtk ./load.vtk")
                    os.system(f"zip -r -qq {folder}.zip ./forces")
                    os.system(f"mv {folder}.zip ./out/{folder}")
                    os.system(f"rm ./forces/*")
os.system("rm load.vtk")
