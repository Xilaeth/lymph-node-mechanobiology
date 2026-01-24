import numpy as np
import matplotlib.pyplot as plt
import sys

path = sys.argv[1]
n = int(sys.argv[2])

tot = []

for i in range(n):
    data_temp = np.loadtxt(f"{path}{i}.csv", delimiter=',')
    fxs = data_temp[::2]
    fys = data_temp[1::2]
    tot.append(np.sqrt(sum(fxs)**2 + sum(fys)**2))

x = np.linspace(0, n-1, n)

plt.scatter(x, tot, s=0.5, c='black')
plt.xlabel("Time Step", fontsize=13)
plt.ylabel("Total Force", fontsize=13)
plt.plot(x, tot, 'r--')
plt.savefig("forces.png")
