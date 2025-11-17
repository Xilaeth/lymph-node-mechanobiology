import os
import sys

tif = "input.tif"
wt = 2000
ht = 2000
w = 501
h = 501
f = 0.17
fr = 0.05

for inp in sys.argv[1:]:
    if (inp[0] == '-'):
        match inp[1:3]:
            case "w=":
                w = int(inp[3:])
                continue
            case "h=":
                h = int(inp[3:])
                continue
            case "f=":
                f = float(inp[3:])
                continue
        match inp[1:4]:
            case "fr=":
                fr = float(inp[4:])
                continue
            case "wt=":
                wt = int(inp[4:])
                continue
            case "ht=":
                ht = int(inp[4:])
                continue
        match inp[1:5]:
            case "tif=":
                tif = inp[5:]
                continue
    else:
        continue

print("Creating tif samples:")
os.system(f"python3 make_parts.py {tif} -w={w} -h={h} -f={fr} -wt={wt} -ht={ht}")

files = os.listdir("out-tif")
l = len(files)
bx = int(0.25*w)
by = int(0.25*h)
os.system(f"python3 2d.py -nx={bx} -ny={by} -l=0.5")

print("Creating the vtks from samples:")
for i in range(l):
    print(f"{i}/{l}")
    os.system(f"cp ./out-tif/{files[i]} ./")
    os.system(f"python3 run-destroy-repulse-outside.py out.vtk -im={files[i]}")
    os.system(f"rm ./{files[i]}")
    os.system(f"python3 add_id.py out_{files[i]}.vtk {files[i][:-4]}")
    os.system(f"rm ./out_{files[i]}.vtk")
    os.system(f"mv {files[i][:-4]}.vtk ./out-vtk")
    
print("Running the simulations:")
for i in range(l):
    print(f"{i}/{l}")
    os.system(f"cp ./out-vtk/{files[i][:-4]}.vtk ./")
    os.system(f"python3 run-small.py {files[i][:-4]} {f}")
    os.system(f"rm ./{files[i][:-4]}.vtk")
