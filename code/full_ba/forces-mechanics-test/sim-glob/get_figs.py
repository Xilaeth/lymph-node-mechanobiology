import os
import sys

folder = sys.argv[1]
folders = os.listdir(folder)
d = sys.argv[2]
n = len(folders)
i = 0

for f in folders:
    i += 1
    print(f"{i}/{n}")
    os.system(f"python3 stretch.py ./data/{f}/out_99.vtk {d}")
    os.system(f"mv out_stretch.csv ./data/{f}")
    os.system(f"python3 v_screen.py ./data/{f}/out_ 100")
    os.system(f"mv ./s0.png ./data/{f}")
    os.system(f"mv ./s100.png ./data/{f}")
