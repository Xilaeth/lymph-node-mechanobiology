import numpy as np
import sys
import matplotlib.pyplot as plt

force_tot = []
varia = []

for i in range(int(sys.argv[2]) + 1):
    data_temp = np.loadtxt(f"{sys.argv[1]}{i}.csv", delimiter=",")
    force_tot.append(sum(data_temp))
    varia.append(np.var(force_tot))

force_tot = np.array(force_tot)

fig, ax = plt.subplots()
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
ax.plot(range(len(force_tot)), force_tot, 'b')
ax.set_xlabel("N")
ax.set_ylabel(r'$F_{tot}(N)$')
plt.savefig(sys.argv[3], bbox_inches='tight')

with open(f"{sys.argv[4]}/forces.csv", "w", encoding="ascii") as f:
    for i in range(len(force_tot)):
        if (i == (len(force_tot) - 1)):
            f.write(str(force_tot[i]))
        else:
            f.write(str(force_tot[i]) + ",")
