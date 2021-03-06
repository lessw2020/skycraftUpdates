from ursina import *

panda=FrameAnimation3d('foxWalk_',fps=4)
panda.texture='fox_tex'
#panda.texture='panda_texture'
#panda=Entity(model='fox',texture='fox_tex')
panda.position=Vec3(5,2,5)
panda.turnSpeed=1
panda.speed=3

def mob_movement(mob,subPos,td):
    tempOR=mob.rotation_y
    mob.lookAt(subPos)
    mob.rotation=Vec3(0,mob.rotation.y+180,0)
    mob.rotation_y=lerp(tempOR,mob.rotation_y,mob.turnSpeed*time.dt)

    closenessDistance=3
    distance=subPos-mob.position
    if distance.length()> closenessDistance:
        mob.position-=mob.forward*mob.speed*time.dt
        mob.resume()
        mob.is_playing=True
    else:
        mob.pause()
        mob.is_playing=False
    terrain_walk(mob,td)

def terrain_walk(mob, _td):
    # Check mob hasn't fallen off the planet ;)

    if mob.y < -100:
        mob.y = 100
        print("I've fallen off!")

    blockFound=False
    step = 4
    height = 1
    x = floor(mob.x+0.5)
    z = floor(mob.z+0.5)
    y = floor(mob.y+0.5)
    for i in range(-step,step):
        if _td.get((x,y+i,z))=='t':
            if _td.get((x,y+i+1,z))=='t':
                target = y+i+height+1
                blockFound=True
                break
            target = y+i+height
            blockFound=True
            break
    if blockFound==True:
        # Step up or down :>
        mob.y = lerp(mob.y, target, 6 * time.dt)
    else:
        # Gravity fall :<
        mob.y -= 9.8 * time.dt    