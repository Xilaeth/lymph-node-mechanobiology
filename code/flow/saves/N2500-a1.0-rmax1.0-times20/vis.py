from vedo import *
from vedo.applications import Browser

path="load_"
pdata=[]
for i in range(0,1):
	p=load(f"{path}{i}.vtk")
	p.point_size(30)
	pdata.append(p)
	
plt = Browser(pdata, size=(2000,2000), bg='white',)
plt.show()
