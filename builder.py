from ursina import Vec3,floor
from config import *

def checkBuild(bsite,td,camf, pos):
    dist=bsite-pos
    mouseInWorld=pos+camf*dist.length()
    mouseInWorld-=camf*0.75
    x=round(mouseInWorld.x)
    y=floor(mouseInWorld.y)
    z=round(mouseInWorld.z)
    if bsite==Vec3(x,y,z):
        y+=1
    if td.get((x,y,z))!='g'and td.get((x,y,z)) is not None:
        return None
    return Vec3(x,y,z)

def gapShell(td,bsite):
    for i in range(6):
        p=bsite + g_sixAxis[i]
        x,y,z=floor(p)
        key=(x,y,z)
        res=td.get(key)
        if res is None:
            td[key]='g'