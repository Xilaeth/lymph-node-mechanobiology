import os
import sys

al = [0.2] #[0.1, 0.2, 0.4]
bl = [1.5] #[1.0, 1.5, 2.0]
req = 1.0
d = 2.0
Ds = [0.0] #[0.0, 0.01, 0.02]
dt = 0.05
Ts = [1000] #, 20, 40, 80, 160, 320]
fs = [0.04] #[0.01, 0.02, 0.04, 0.08, 0.16]
fd = 1
#file = sys.argv[1]
files = [sys.argv[1]]
n = len(al)*len(bl)*len(Ds)*len(files)*len(fs)*len(Ts)
c = 0
m = sys.argv[2]

for file in files:
    for a in al:
        for b in bl:
            for D in Ds:
                for f in fs:
                    for T in Ts:
                        en = int(T/100)
                        c += 1
                        print(f"{c}/{n}")
                        name = f"inp-{file}_T-{T}_dt-{dt}_a-{a}_b-{b}_req-{req}_d-{d}_D-{D}_f-{f}_fdir-{fd}"
                        os.system(f"mkdir ./out/{name}")
                        os.system(f"python3 run-param-move.py {file}.vtk -a={a} -b={b} -d={d} -req={req} -T={T} -D={D} -dt={dt} -en={en} -f={f} -fd={fd} -m={m}")
                        os.system(f"mv ./output/* ./out/{name}")
