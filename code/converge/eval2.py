import numpy as np
import sys
import matplotlib.pyplot as plt

force_tot = []
varia = []

data_temp = np.loadtxt(f"{sys.argv[1]}", delimiter=",")
force_tot = np.array(list(map(float, data_temp)))

avg = np.mean(force_tot)
var = np.var(force_tot)

print(f"avg: {avg}")
print(f"var: {var}")
print(f"var/avg: {var/avg}")
