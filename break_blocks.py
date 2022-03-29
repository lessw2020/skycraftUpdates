
from ursina import Entity,color,floor,Vec3

lookBlock=Entity(model='block.obj',color=color.rgba(1,1,0,0.4))
lookBlock.scale*=1.07
lookBlock.origin_y+=0.05

def mine(td,vd,subsets):
    if not lookBlock.visible: return
    cv=vd.get((floor(lookBlock.x),
               floor(lookBlock.y),
                floor(lookBlock.z)))
    if cv is None:
        return

    for v in range(cv[1]+1,cv[1]+37):
        subsets[cv[0]].model.vertices[v][1]+=999
    subsets[cv[0]].model.generate()

    td[(floor(lookBlock.x),
                floor(lookBlock.y),
                    floor(lookBlock.z))]='g'
    vd[(floor(lookBlock.x),
                floor(lookBlock.y),
                    floor(lookBlock.z))]=None

    return (lookBlock.position,cv[0])


def highlight(pos,cam,td):
    for i in range(1,32):
        wp=pos+Vec3(0,1.86,0)+cam.forward*(i*0.5)
        x=round(wp.x)
        y=floor(wp.y)
        z=round(wp.z)
        lookBlock.x=x
        lookBlock.y=y
        lookBlock.z=z

        if td.get((x,y,z))=='t':
            lookBlock.visible=True
            break
        else:
            lookBlock.visible=False


