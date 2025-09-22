import os

dt_list = [0.01] #, 0.05, 0.1, 0.5, 1.0]
a_list = [1.0] #[0.2, 0.5, 1.0, 2.0, 5.0]
n_list = [10000] #[900, 1600, 2500, 10000, 40000]
rmax = 1.0
T = 10
tot_saves = 100
r_start = 0.48

for dt in dt_list:
    for a in a_list:
        for n in n_list:
            i = 0
            while (True):
                every_n = int(int(T/dt) / tot_saves)
                if (i == 0):
                    folder = f"0-{int(T/dt)}_dt-{dt}_a-{a}_n-{n}"
                    os.system(f"mkdir ./out/{folder}")
                    os.system(f"python3 run_param.py {n} {a} {rmax} {int(T/dt)} {dt} {every_n} {r_start}")
                    os.system(f"python3 read-all.py ./output/out_ {tot_saves} ./forces")
                    os.system(f"rm ./output/*")
                    os.system(f"python3 eval.py ./forces/forces {tot_saves} ./out/{folder}/convergence_0-{int(T/dt)}_dt-{dt}.png ./out/{folder}")
                    os.system(f"cp ./forces/positions{tot_saves}.vtk ./")
                    os.system(f"mv ./positions{tot_saves}.vtk ./load.vtk")
                    os.system(f"zip -r -qq {folder}.zip ./forces")
                    os.system(f"mv {folder}.zip ./out/{folder}")
                    os.system(f"rm ./forces/*")
                else:
                    folder = f"{i*int(T/dt)}-{(i+1)*int(T/dt)}_dt-{dt}_a-{a}_n-{n}"
                    os.system(f"mkdir ./out/{folder}")
                    os.system(f"python3 run_param_load.py load.vtk {a} {rmax} {int(T/dt)} {dt} {every_n}")
                    os.system(f"python3 read-all.py ./output/out_ {tot_saves} ./forces")
                    os.system(f"rm ./output/*")
                    os.system(f"python3 eval.py ./forces/forces {tot_saves} ./out/{folder}/convergence_{i*int(T/dt)}-{(i+1)*int(T/dt)}_dt-{dt}.png ./out/{folder}")
                    os.system(f"cp ./forces/positions{tot_saves}.vtk ./")
                    os.system(f"mv ./positions{tot_saves}.vtk ./load.vtk")
                    os.system(f"zip -r -qq {folder}.zip ./forces")
                    os.system(f"mv {folder}.zip ./out/{folder}")
                    os.system(f"rm ./forces/*")
                    conv = os.popen(f"python3 check_conv.py ./out/{folder}/forces.csv").read()
                    if (int(conv) == 1):
                        break
                i += 1
                if (i > 10):
                    break
os.system("rm load.vtk")
