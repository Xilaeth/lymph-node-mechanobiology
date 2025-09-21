import numpy as np
import sys
import matplotlib.pyplot as plt

force_tot = []
varia = []

for i in range(int(sys.argv[2]) + 1):
    data_temp = np.loadtxt(f"{sys.argv[1]}{i}.csv", delimiter=",")
    force_tot.append(sum(data_temp))
    varia.append(np.var(force_tot))

force_tot = np.array(force_tot)/max(force_tot)
#varia = np.array(varia)/max(varia)

plt.plot(range(len(force_tot)), force_tot, 'b')
#plt.plot(range(len(force_tot)), varia, 'r-')
plt.show()
