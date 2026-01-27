import os
import sys

al = [0.2] #[0.1, 0.2, 0.4]
a2l = [0.0] #[0.1, 0.2, 0.4]
bl = [1.5] # 2.0] #[1.0, 1.5, 2.0]
req = 1.0
ds = [2.0]#, 3.0]
Ds = [0.0] #[0.0, 0.01, 0.02]
dt = 0.05
Ts = [10]
fs = [0.08] #, 0.02, 0.04, 0.08, 0.16]
fd = 1
#file = sys.argv[1]
files = [sys.argv[1]]
n = len(al)*len(a2l)*len(bl)*len(Ds)*len(files)*len(fs)*len(Ts)*len(ds)
c = 0
N = 30

for file in files:
    for a in al:
        for a2 in a2l:
            for b in bl:
                for D in Ds:
                    for f in fs:
                        for T in Ts:
                            for d in ds:
                                en = T 
                                c += 1
                                print(f"{c}/{n}")
                                name = f"inp-{file}_T-{T}_dt-{dt}_a-{a}_b-{b}_req-{req}_d-{d}_D-{D}_f-{f}_fdir-{fd}"
                                os.system(f"mkdir ./out/{name}")
                                os.system(f"python3 run-param-track-beads.py {file}.vtk -a={a} -b={b} -d={d} -req={req} -T={T} -D={D} -dt={dt} -en={en} -f={f} -fd={fd} -a2={a2}")
                                os.system(f"mv ./output/* ./out/{name}")
                                os.system(f"python3 make_dif.py {file}.vtk ./out/{name} {name}")
                                os.system(f"mv {name}.csv ./out/{name}")
                                os.system(f"python3 vis_dif_beads_scr.py {file}.vtk ./out/{name}/{name}.csv {fd}")
                                os.system(f"mv difs.png ./out/{name}")
os.system("mv ./out/* ./data")
