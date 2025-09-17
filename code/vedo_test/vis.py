from vedo import *
from vedo.applications import Browser

pdata=[]
p=load(f"test.vtk")
p.point_size(60)
pdata.append(p)
	
plt = Browser(pdata, size=(2000,2000), bg='white',)
plt.show()
