import os
import sys

folder = sys.argv[1]
folders = os.listdir(folder)
n = len(folders)
i = 0

for f in folders:
    i += 1
    print(f"{i}/{n}")
    os.system(f"python3 read-all.py {folder}/{f}/out_ 100 split")
    os.system(f"mv {folder}/{f} ./data")
    os.system(f"mv ./split ./data/{f}")
    os.system(f"python3 v_screen.py ./data/{f}/out_ 101")
    os.system(f"mv ./s0.png ./data/{f}")
    os.system(f"mv ./s100.png ./data/{f}")
    os.system(f"python3 v_for.py ./data/{f}/split/forces 101")
    os.system(f"mv ./forces.png ./data/{f}")
    os.system("mkdir split")
