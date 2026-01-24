import os
import sys

al = [0.2] #[0.1, 0.2, 0.4]
bl = [1.5] #[1.0, 1.5, 2.0]
req = 1.0
d = 2.0
Ds = [0.0] #[0.0, 0.01, 0.02]
dt = 1.0
Ts = [25000] #, 20, 40, 80, 160, 320]
Fs = [1.0, 2.0, 5.0, 10.0, 20.0, 50.0] #, 0.02, 0.04, 0.08, 0.16]
fd = 2
ids = 2
fra = 0.1

#file = sys.argv[1]
files = [sys.argv[1]]
n = len(al)*len(bl)*len(Ds)*len(files)*len(Fs)*len(Ts)
c = 0
N = int(os.popen(f"python3 get_num.py {files[0]}.vtk").read())

for file in files:
    for a in al:
        for b in bl:
            for D in Ds:
                for F in Fs:
                    for T in Ts:
                        en = int(T/100)
                        c += 1
                        f = float(F/N)
                        print(f"{c}/{n}")
                        name = f"inp-{file}_T-{T}_dt-{dt}_a-{a}_b-{b}_req-{req}_d-{d}_D-{D}_F-{F}_N-{N}_fdir-{fd}_id-{ids}"
                        os.system(f"mkdir ./out/{name}")
                        os.system(f"python3 run-param-track.py {file}.vtk -a={a} -b={b} -d={d} -req={req} -T={T} -D={D} -dt={dt} -en={en} -f={f} -fd={fd} -id={ids}")
                        os.system(f"mv ./output/* ./out/{name}")
os.system(f"mv ./out/* ./data")
