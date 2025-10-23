import os 
import sys

nxs = [2, 20]
nys = [10, 100]
ass = [0.5, 1.0]
rms = [1.0]
Fs = [1.0]
fs = [0.04, 0.4]
modes = [1]
T = 10000
dt = 0.05
en = 1000

i = 0
tot = len(nxs)*len(nys)*len(ass)*len(rms)*len(Fs)*len(fs)*len(modes)

for nx in nxs:
    for ny in nys:
        for a in ass:
            for rm in rms:
                for F in Fs:
                    for f in fs:
                        for m in modes:
                            i += 1
                            print(f"{i}/{tot}")
                            name = f"nx-{nx}_ny-{ny}_a-{a}_rm-{rm}_F-{F}_f-{f}_T-{T}_dt-{dt}_en-{en}_m-{m}"
                            os.system(f"mkdir out/{name}")
                            os.system(f"python3 2d.py -nx={nx} -ny={ny} -l=0.5")
                            os.system(f"python3 add_id.py out.vtk init {m}")
                            num = int(os.popen(f"python3 count.py init.vtk").read())
                            f = f/num
                            os.system(f"cp init.vtk ./out/{name}")
                            os.system(f"python3 run_param_load.py init.vtk -a={a} -rm={rm} -f={f} -F={F} -T={T} -dt={dt} -en={en}")
                            os.system(f"mv output ./out/{name}")
                            os.system(f"rm init.vtk")
                            os.system(f"mkdir output")
