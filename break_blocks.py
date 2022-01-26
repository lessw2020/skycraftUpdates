

from re import sub
from ursina import Entity,color,floor,Vec3


lookBlock=Entity(model='cube',color=color.rgba(1,1,0,0.4))
lookBlock.scale*=1.001

def mine(td,vd,subsets):
    if not lookBlock.visible: return
    cv=vd.get((floor(lookBlock.x),
               floor(lookBlock.y-0.5),
                floor(lookBlock.z)))
    if cv is None:
        return
    for v in range(cv[1]+1,cv[1]+37):
        subsets[cv[0]].model.vertices[v][1]+=999
    subsets[cv[0]].model.generate()
    td[(floor(lookBlock.x),
                floor(lookBlock.y-0.5),
                    floor(lookBlock.z))]='g'
    vd[(floor(lookBlock.x),
                floor(lookBlock.y-0.5),
                    floor(lookBlock.z))]=None

    return (lookBlock.position+Vec3(0,-0.5,0),cv[0])


def higlight(pos,cam,td):
    for i in range(1,15):
        wp=pos+cam.forward*i
        x=floor(wp.x)
        y=floor(wp.y+3)
        z=floor(wp.z)
        lookBlock.x=x
        lookBlock.y=y+0.5
        lookBlock.z=z

        if td.get((x,y,z))=='t':
            lookBlock.visible=True
            break
        else:
            lookBlock.visible=False


