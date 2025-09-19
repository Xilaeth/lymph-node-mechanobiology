import numpy as np
import sys

data = np.loadtxt(sys.argv[1], delimiter=",")

print(f"{np.mean(data)} {np.var(data)}")
