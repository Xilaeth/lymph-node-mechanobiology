import os

N = 2500
rect = 50
a = 1.0
r_max = 1.0
n_times = 20 # 550 time steps in total

os.system(f"./relax {N} {a} {r_max} {rect} >> force0.csv")
os.system("mv ./output/relax_0.vtk ./")
os.system("mv ./relax_0.vtk ./load_0.vtk")
for i in range(1, n_times + 1):
    print(i)
    os.system(f"./load {a} {r_max} load_0.vtk >> force{i}.csv")
    os.system("mv ./output/load_0.vtk ./")
os.system(f"mkdir ./saves/N{N}-a{a}-rmax{r_max}-times{n_times}")
os.system(f"mv ./load_0.vtk ./saves/N{N}-a{a}-rmax{r_max}-times{n_times}")
os.system(f"mv ./*.csv ./saves/N{N}-a{a}-rmax{r_max}-times{n_times}")
