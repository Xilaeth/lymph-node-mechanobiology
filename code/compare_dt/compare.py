import os
import sys

dt_list = [0.01, 0.05, 0.1, 0.5, 1.0]
n = 2500
a = 1.0
rmax = 1.0
T = 2500*0.05
every_n = 1
r_start = 0.45

for dt in dt_list:
    os.system(f"mkdir ./out/dt-{dt}")
    os.system(f"python3 run_param.py {n} {a} {rmax} {int(T/dt)} {dt} {every_n} {r_start}")
    os.system(f"python3 read-all.yp ./output/out_ {int(T/dt)} ./forces")
    os.system("rm -r ./output/*")
    os.system(f"zip -r dt-{dt}.zip ./forces")
    os.system(f"mv ./dt-{dt}.zip ./out/dt-{dt}")
    os.system(f"python3 eval.py ./forces/forces {int(T/dt)} ./out/dt-{dt}/convergence-{dt}.png")
    os.system("rm -r ./forces/*)
