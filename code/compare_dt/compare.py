import os

dt_list = [0.01] #, 0.05, 0.1, 0.5, 1.0]
a_list = [1.0] #[0.2, 0.5, 1.0, 2.0, 5.0]
n_list = [40000] #[900, 1600, 2500, 10000, 40000]
rmax = 1.0
T = 500
tot_saves = 200
r_start = 0.45

#for dt in dt_list:
#    print(f"starting with: {dt}")
#    os.system(f"mkdir ./out/dt-{dt}")
#    os.system(f"python3 run_param.py {n} {a} {rmax} {int(T/dt)} {dt} {every_n} {r_start}")
#    os.system(f"python3 read-all.py ./output/out_ {int(T/dt)} ./forces")
#    os.system("rm -r ./output/*")
#    os.system(f"python3 eval.py ./forces/forces {int(T/dt)} ./out/dt-{dt}/convergence-{dt}.png")
#    os.system(f"zip -r dt-{dt}.zip ./forces")
#    os.system(f"mv ./dt-{dt}.zip ./out/dt-{dt}")
#    os.system("rm -r ./forces/*")

#for a in a_list:
#    print(f"starting with: {a}")
#    os.system(f"mkdir ./out/a-{a}")
#    os.system(f"python3 run_param.py {n} {a} {rmax} {int(T/dt)} {dt} {every_n} {r_start}")
#    os.system(f"python3 read-all.py ./output/out_ {int(T/dt)} ./forces")
#    os.system("rm -r ./output/*")
#    os.system(f"python3 eval.py ./forces/forces {int(T/dt)} ./out/a-{a}/convergence-{a}.png")
#    os.system(f"zip -r a-{a}.zip ./forces")
#    os.system(f"mv ./a-{a}.zip ./out/a-{a}")
#    os.system("rm -r ./forces/*")

for dt in dt_list:
    for a in a_list:
        for n in n_list:
            every_n = int(int(T/dt) / tot_saves)
            print(f"starting with: {n}-{dt}-{a}")
            os.system(f"mkdir ./out/n-{n}_dt-{dt}_a-{a}")
            os.system(f"python3 run_param.py {n} {a} {rmax} {int(T/dt)} {dt} {every_n} {r_start}")
            os.system(f"python3 read-all.py ./output/out_ {tot_saves} ./forces")
            os.system("rm -r ./output/*")
            os.system(f"python3 eval.py ./forces/forces {tot_saves} ./out/n-{n}_dt-{dt}_a-{a}/convergence-n-{n}-dt-{dt}_a-{a}.png")
            os.system(f"zip -r n-{n}_dt-{dt}_a-{a}.zip ./forces")
            os.system(f"mv ./n-{n}_dt-{dt}_a-{a}.zip ./out/n-{n}_dt-{dt}_a-{a}")
            os.system("rm -r ./forces/*")
