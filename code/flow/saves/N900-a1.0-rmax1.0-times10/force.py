import numpy as np
import matplotlib.pyplot as plt

Fs = []
FsVar = []
n = 10
T = 100

for i in range(n + 1):

    file = open(f"force{i}.csv", "rt")
    content = file.read()
    lines = content.splitlines()[:-2]

    # we create a list of the type [[x1, y1], [x2, y2],...]
    data = list(map(lambda x: list(map(lambda y: float(y), x.split(',')[:-1])), lines))

    xs = list(map(lambda x: x[0::3], data)) 
    ys = list(map(lambda x: x[1::3], data)) 
    zs = list(map(lambda x: x[2::3], data))

    Ftot = []

    for i in range(len(xs)):
        Ftot.append(0)
        for j in range(len(xs)):
            Ftot[i] += xs[i][j]**2 + ys[i][j]**2 + zs[i][j]**2

    Fs.extend(Ftot)
    FsVar.append(np.var(Fs))


#print(Fs)
plt.plot(range(len(FsVar)), FsVar)
plt.show()
