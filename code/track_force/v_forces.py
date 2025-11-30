import numpy as np
import matplotlib.pyplot as plt
import sys

path = sys.argv[1]
n = int(sys.argv[2])

tot = []

for i in range(n):
    data_temp = np.loadtxt(f"{path}{i}.csv", delimiter=',')
    tot.append(sum(data_temp))

x = np.linspace(0, 100, 101)

plt.scatter(x, tot, s=0.5, c='black')
plt.plot(x, tot, 'r--')
plt.show()
