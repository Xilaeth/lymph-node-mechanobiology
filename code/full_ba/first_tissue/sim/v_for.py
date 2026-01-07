import numpy as np
import matplotlib.pyplot as plt
import sys

path = sys.argv[1]
n = int(sys.argv[2])

tot = []

for i in range(n):
    data_temp = np.loadtxt(f"{path}{i}.csv", delimiter=',')
    tot.append(sum(data_temp))

x = np.linspace(0, n-1, n)

plt.scatter(x, tot, s=0.5, c='black')
plt.xlabel("Time Step", fontsize=13)
plt.xlabel("Total Force", fontsize=13)
plt.plot(x, tot, 'r--')
plt.savefig("forces.png")
