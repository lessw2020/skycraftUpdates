
# this will make snow flakes :D

from ursina import Entity,Vec3,time
from random import random

totalSnowflakes=512

class Flake(Entity):
    sub=None

    @staticmethod
    def setSub(subjectEntity):
        Flake.sub= subjectEntity

    def __init__(self,orig):
        super().__init__(model='quad',
        texture='flake_1.png',
        position=orig,
        scale=0.2,
        double_sided=True
        )
        self.x+=random()*20-10 
        self.z+=random()*20-10
        self.y+=random()*10+5

        minSpeed=1
        self.fallSpeed=random()*4+minSpeed

        minSpin=100
        self.spinSpeed=random()*40+minSpin

    def update(self,):
        self.physics()

    def physics(self):
        subPos=Flake.sub.position
        self.y-=self.fallSpeed*time.dt
        self.rotation_y+=self.spinSpeed*time.dt

        if self.y<0:
            self.x=subPos.x+(random()*20-10)
            self.z=subPos.z+(random()*20-10)
            self.y=subPos.y+(random()*10+5)

class snowFall():
    def __init__(self, subRuf):
        self.flakes=[]
        Flake.setSub(subRuf)
        for i in range(totalSnowflakes):
            e=Flake(subRuf.position)
            self.flakes.append(e)