import os

N = 10000
rect = 100
a = 1.0
r_max = 1.0
n_times = 20

os.system(f"./relax {N} {a} {r_max} {rect}")
os.system("mv ./output/relax_0.vtk ./")
os.system("mv ./relax_0.vtk ./load_0.vtk")
for i in range(1, n_times + 1):
    print(i)
    os.system(f"./load {a} {r_max} load_0.vtk")
    os.system("mv ./output/load_0.vtk ./")
os.system(f"mkdir ./saves/N{N}-a{a}-rmax{r_max}-times{n_times}")
os.system(f"mv ./load_0.vtk ./saves/N{N}-a{a}-rmax{r_max}-times{n_times}")
#os.system(f"mv ./*.csv ./saves/N{N}-a{a}-rmax{r_max}-times{n_times}")
#os.system(f"python3 force.py saves/N{N}-a{a}-rmax{r_max}-times{n_times} {n_times}")
#os.system(f"rm saves/N{N}-a{a}-rmax{r_max}-times{n_times}/force*.csv")
