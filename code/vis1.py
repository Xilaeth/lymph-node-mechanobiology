from vedo import *
from vedo.applications import Browser
import sys

path=sys.argv[1]
pdata=[]
p=load(f"{path}")
p.point_size(5)
p.color("green")
pdata.append(p)
	
plt = Browser(pdata, size=(2000,2000), bg='white',)
plt.show()
