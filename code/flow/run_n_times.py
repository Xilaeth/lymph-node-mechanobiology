import os

N = 10000
rect = 100
a = 2.5
r_max = 1.0
n_times = 10 # 550 time steps in total

os.system(f"./relax {N} {a} {r_max} {rect}")
os.system("mv ./output/relax_0.vtk ./")
os.system("mv ./relax_0.vtk ./load_0.vtk")
for i in range(n_times):
    print(i)
    os.system(f"./load {a} {r_max} load_0.vtk")
    os.system("mv ./output/load_0.vtk ./")
