from vedo import *
from vedo.applications import Browser
import sys

pdata=[]
for i in range(0,1):
	p=load(f"{sys.argv[1]}")
	p.point_size(10)
	pdata.append(p)
	
plt = Browser(pdata, size=(2000,2000), bg='white',)
plt.show()
