from vedo import *
from vedo.applications import Browser

path="output/test"
pdata=[]
for i in range(0,100):
	p=load(f"{path}{i}.vtk")
	p.point_size(60)
	pdata.append(p)
	
plt = Browser(pdata, size=(2000,2000), bg='white',)
plt.show()
