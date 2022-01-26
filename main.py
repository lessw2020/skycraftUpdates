from typing import Counter
from ursina import *
from numpy import abs, true_divide
from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrain import Meshterrain
from flakes import snowFall

app=Ursina()
window.color=color.rgb(179,232,255)
skyStuff=Sky()
skyStuff.color=window.color
player=FirstPersonController()
player.gravity= 0
player.cursor.visible=False
#window.fullscreen=True
count=0
pX=player.x
pZ=player.z

terrain=Meshterrain()
snowFall=snowFall(player)

def input(key):
    terrain.input(key)



def update():
    global count,pX,pZ
    terrain.genTerrain()
    count+=1
    if count==4:
        count=0
        terrain.update(player.position,camera)

        
    if abs(player.x-pX)>4 or abs(player.z-pZ)>4:
        pX=player.x
        pZ=player.z
        terrain.Swirl.reset(pX,pZ)


    blockFound=False
    step=2
    height=1.86
    x=floor(player.x+0.5)
    y=floor(player.y+0.5)
    z=floor(player.z+0.5)

    for i in range(-step,step):
        if terrain.td.get((x,y+i,z))=="t":
            if terrain.td.get((x,y+i+1,z))=="t":
                target=y+i+height+1
                blockFound=True
                break
            target=y+i+height
            blockFound=True
            break

    if blockFound== True:
        player.y=lerp(player.y,target,6*time.dt)
    else:

        player.y-=9.8*time.dt 
terrain.genTerrain()
fox=Entity(model='fox', texture='fox')
fox.position=Vec3(0,2,11)
app.run()