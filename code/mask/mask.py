import numpy as np
import matplotlib.pyplot as plt

file = open("n1600T10000dt05.vtk", "rt")
content = file.read()
lines = content.splitlines()
lines = lines[6:]

coords = list(map(lambda x: list(map(lambda y: float(y), x.split(' ')))[:2], lines))
xs = list(map(lambda x: x[0], coords))
ys = list(map(lambda x: x[1], coords))

def isInSquare(x, l, v):
    if ((abs(v[0] - x[0]) < l/2) and (abs(v[1] - x[1]) < l/2)):
        return True
    return False

def densityInSquare(x, l):
    counter = 0
    for i in range(len(xs)):
        if (isInSquare(x, l, coords[i])):
            counter += 1

    return (counter / (l*l))

#print(densityRatio(15))

plt.scatter(xs, ys, s=1.5, c='red')
plt.show()

