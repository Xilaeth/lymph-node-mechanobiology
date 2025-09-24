import os
import sys
from math import sqrt

n = 2500
a = 1.0
rmax = 1.0
T = 1000
dt = 0.01
every_n = 1
starting_dist = 0.45
D = 0.01

for inp in sys.argv[1:]:
    if (inp[0] == '-'):
        match inp[1:3]:
            case "n=":
                n = inp[3:]
                continue
            case "a=":
                a = inp[3:]
                continue
            case "T=":
                T = inp[3:]
                continue
            case "D=":
                D = inp[3:]
                continue
        match inp[1:4]:
            case "dt=":
                dt = inp[4:]
                continue
            case "en=":
                every_n = inp[4:]
                continue
            case "sd=":
                starting_dist = inp[4:]
                continue
            case "rm=":
                rmax = inp[4:]
                continue

rect = sqrt(n)

os.system(f"./relax {n} {a} {rmax} {rect} {T} {dt} {every_n} {starting_dist} {D}")
