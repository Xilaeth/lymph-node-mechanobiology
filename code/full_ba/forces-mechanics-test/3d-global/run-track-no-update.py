import os
import sys

files = []

for inp in sys.argv[1:]:
    if (inp[0:3] == '-f='):
        files.append(inp[3:])

al = [0.2] #[0.1, 0.2, 0.4]
bl = [1.5] #[1.0, 1.5, 2.0]
req = 1.0
d = 2.0
Ds = [0.0] #[0.0, 0.01, 0.02]
dt = 1.0
Ts = [25000] #, 20, 40, 80, 160, 320]
Fs = [64.0, 128.0, 10, 12, 14, 18, 20, 3.0, 5.0, 6.0, 7.0, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0]
fd = 2
ids = 2
fra = 0.1

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
                        os.system(f"python3 run-param-track-no-update.py {file}.vtk -a={a} -b={b} -d={d} -req={req} -T={T} -D={D} -dt={dt} -en={en} -f={f} -fd={fd} -id={ids}")
                        os.system(f"mv ./output/* ./out/{name}")
os.system(f"mv ./out/* ./data")
