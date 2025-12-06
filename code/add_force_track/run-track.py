import os
import sys

al = [0.8]
D = 0.0
dt = 0.01
T = 20000
en = int(T/100)
#file = sys.argv[1]
files = ["out_lines_125-125-no-edge", "out_lines_68-68-no-edge"]
c = 0

#force = float(sys.argv[2])
fracs = [1.0]
fs = [0.5, 1.0, 2.0, 4.0, 8.0, 16.0]
n = len(al)*len(files)*len(fracs)*len(fs)

for a in al:
    for frac in fracs:
        for file in files:
            N = float(os.popen(f"python3 count.py {file}.vtk").read())
            for ft in fs:
                f = ft*float(1/N)
                c += 1
                print(f"{c}/{n}")
                name = f"inp-{file}_T-{T}_dt-{dt}_a-{a}_D-{D}_f-{f}_N-{N}"
                os.system(f"mkdir ./out/{name}")
                os.system(f"python3 run-param-track.py {file}.vtk -a={a} -T={T} -D={D} -dt={dt} -en={en} -fr={frac} -fo={f}")
                os.system(f"mv ./output/* ./out/{name}")
