from typing import Counter
from ursina import *
app=Ursina()


from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrain import Meshterrain
from flakes import snowFall
from mobMove import *
from inventory import *

window.color=color.rgb(179,232,255)
skyStuff=Sky()
skyStuff.color=window.color
player=FirstPersonController()
player.gravity= 0
player.cursor.visible=False

startLandSize=64
count=0
pX=player.x
pZ=player.z

terrain=Meshterrain(player,camera)
genTerrainFunction=terrain.genTerrain
#snowFall=snowFall(player)
for i in range(startLandSize):
    genTerrainFunction()    
generatingTerrain=True
def input(key):
    global generatingTerrain
    terrain.input(key)
    if key=='g':
        generatingTerrain=not generatingTerrain
        
    inv_input(key,player,mouse)

#count=0
def update():
    global count,pX,pZ,genTerrainFunction
    terrain.update(player.position,camera)
    mob_movement(panda,player.position,terrain.td)
    count+=1
    if count==2:
        count=0
        if generatingTerrain:
            genTerrainFunction()
    if abs(player.x-pX)>4 or abs(player.z-pZ)>4:
        pX=player.x
        pZ=player.z
        terrain.swirlEngine.reset(pX,pZ)


    blockFound=False
    step=2
    height=1.86
    x=floor(player.x+0.5)
    y=floor(player.y+0.5)
    z=floor(player.z+0.5)
    ptrTd=terrain.td
    for i in range(-step,step):
        if ptrTd.get((x,y+i,z))=="t":
            if ptrTd.get((x,y+i+1,z))=="t":
                target=y+i+height+1
                blockFound=True
                break
            target=y+i+height
            blockFound=True
            break
        
    if blockFound:
        player.y=lerp(player.y,target,6*time.dt)
    else:

        player.y-=9.8*time.dt 
terrain.genTerrain()


app.run()