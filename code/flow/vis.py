from vedo import *
from vedo.applications import Browser
import sys

path=sys.argv[1]
pdata=[]
for i in range(int(sys.argv[2]), int(sys.argv[3])):
	p=load(f"{path}{i}.vtk")
	p.point_size(30)
	pdata.append(p)
	
plt = Browser(pdata, size=(2000,2000), bg='white',)
plt.show()
