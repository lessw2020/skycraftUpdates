from ursina import Vec3,floor
from config import *

def checkBuild(key,bsite,td):
    bepi=bsite+Vec3(0,-0.5,0)
    x,y,z=floor(bepi)
    y+=1
    key=(x,y,z)
    res=td.get(key)
    if res is None or res=='g':
        return Vec3(x,y,z)
    else:
        return None

def gapShell(td,bsite):
    for i in range(6):
        p=bsite + g_sixAxis[i]
        x,y,z=floor(p)
        key=(x,y,z)
        res=td.get(key)
        if res is None:
            td[key]='g'