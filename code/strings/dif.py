import os
import sys

folder = sys.argv[1]

n = len([name for name in os.listdir(f"./out/{folder}/output/")]) - 1

q1 = float(os.popen(f"python3 quant-stretch.py ./out/{folder}/init.vtk").read())
q2 = float(os.popen(f"python3 quant-stretch.py ./out/{folder}/output/out_{n}.vtk").read())

if (q1 == 0):
    print(-1)
else:
    print(q2/q1)
