import numpy as np
import matplotlib.pyplot as plt
import sys

path = sys.argv[1]
n = int(sys.argv[2])

avg = []

for i in range(n):
    data_temp = np.loadtxt(f"{path}{i}.csv", delimiter=',')
    avg.append(np.mean(data_temp))

x = np.linspace(0, 100, 101)

plt.scatter(x, avg, s=0.5, c='black')
plt.plot(x, avg, 'r--')
plt.show()
