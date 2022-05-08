from typing import Counter
from ursina import *
app=Ursina()
g_step=1/255

from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrain import Meshterrain
from flakes import snowFall
from mobMove import *
from inventory import *

daySky='daySky.jpg'
nightSky='nightSky.jpeg'
#window.color=color.rgb(179,232,255)
window.color=color.rgb(30,30,40)
skyStuff=Sky(texture=daySky)
#Sky(texture='nightSky.jpeg')
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
timeSlower=2
timeFilter=0
gettingBrighter=True
maxBright=220
minBright=50
timeCount=0
daytime=True
daycycle=0
timeDiff=maxBright-minBright
def update():
    global timeFilter, timeSlower, timeDiff, gettingBrighter, count,pX,pZ,genTerrainFunction, daycycle, daytime,maxBright, minBright,timeCount
    terrain.update(player.position,camera)
    mob_movement(panda,player.position,terrain.td)
    count+=1
    timeCount+=1
    timeFilter+=1
    if timeFilter==timeSlower:
        timeFilter=0
        if gettingBrighter:

            window.color[0]+=g_step
            window.color[1]+=g_step
            window.color[2]+=g_step
            daycycle+=1
        else:
            window.color[0]-=g_step
            window.color[1]-=g_step
            window.color[2]-=g_step
            daycycle+=1

        if timeCount%timeDiff==0:

            gettingBrighter=not gettingBrighter

            
        skyStuff.color=window.color
        print(f'daycycle is {daycycle}')
        if daycycle==timeDiff*2:
            skyStuff.texture=nightSky
        elif daycycle>=timeDiff*4:
            skyStuff.texture=daySky
            daycycle=0

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