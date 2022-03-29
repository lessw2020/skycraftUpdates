from random import random
from ursina import *
from perlin import Perlin
from perlin_module import PerlinNoise
from infiniteTerrain import swirlEngine
from break_blocks import *
from builder import *

defaultBlock='grass'

class Meshterrain:
    def __init__(self,sub,cam):
        self.player=sub
        self.camera=cam
        self.subsets=[]
        self.numSubsets=256

        self.subWidth=4
        self.Swirl=swirlEngine(self.subWidth)
        self.currentSubset=0
        self.block=load_model('block.obj')
        self.numVertices=len(self.block.vertices)
        

        self.textureAtlas='texture_atlas_3.png'
        self.td={}
        self.vd={}

        self.perlin=Perlin()
        for i in range(0,self.numSubsets):
            e=Entity(model=Mesh(),
            texture=self.textureAtlas)
            e.texture_scale*=64/e.texture.width

            self.subsets.append(e)


    def update(self, pos,cam):
        highlight(pos,cam,self.td)
        if lookBlock.visible:
            if held_keys['shift'] and held_keys['left mouse']:
                self.do_mining
               
    def do_mining(self):
        epi=mine(self.td,self.vd,self.subsets)
        if epi is not None:
            self.genWalls(epi[0],epi[1])
            self.subsets[epi[1]].model.generate()


    def input(self,key):
        if key=='left mouse up' and lookBlock.visible:
            self.do_mining()

        if key=='right mouse up'and lookBlock.visible==True:
            bsite= checkBuild(lookBlock.position,self.td,self.camera.forward,self.player.position+Vec3(0,self.player.height,0))
            if bsite is not None:
                self.genBlock(floor(bsite.x),floor(bsite.y),floor(bsite.z),subset=0,blockType=defaultBlock)
                gapShell(self.td,bsite)
                self.subsets[0].model.generate()

    def genWalls(self,epi,subset):
        if epi==None : return
        wp=[
            Vec3(0,1,0),
            Vec3(0,-1,0),
            Vec3(-1,0,0),
            Vec3(1,0,0),
            Vec3(0,0,-1),
            Vec3(0,0,1),
        ]
        for i in range(6):
            np=epi+wp[i]
            if self.td.get((floor(np.x),
                            floor(np.y),
                            floor(np.z)))==None:
                            self.genBlock(np.x,np.y,np.z,subset,gap=False,blockType='soil')

    def genBlock(self,x,y,z,subset =-1,gap=True,blockType=defaultBlock):
        if subset==-1:
            subset=self.currentSubset
        
        model=self.subsets[subset].model
        model.vertices.extend([Vec3(x,y,z)+v for v in self.block.vertices])
        
        c=random.random()-0.5

        model.colors.extend((Vec4(1-c,1-c,1-c,1),)*self.numVertices)
        if blockType=='grass':
            uu=8
            uv=7
        elif blockType=='soil':
            uu=10
            uv=7
            if random.random()>.5:
                uu=8
                uv=5
        elif blockType=='stone':
            uu=8
            uv=5
        if y > 2 or blockType=='snow':
            uu=8
            uv=6
        model.uvs.extend([Vec2(uu,uv)+u for u in self.block.uvs])
        self.td[(floor(x),
                floor(y),
                floor(z)
                )] ='t'
        if gap==True:
            key=(floor(x),
                floor(y+1),
                floor(z)
                ) 
            if self.td.get(key)==None:
                self.td[key]='g'
        
        vob=(subset,len(model.vertices)-37)
        self.vd[(floor(x),
                floor(y),
                floor(z)
                )] = vob
        


    def genTerrain(self):
        x = floor(self.Swirl.pos.x)
        z = floor(self.Swirl.pos.y)
        d = self.subWidth//2
        for k in range(-d,d):
            for j in range(-d,d):
                y=floor(self.perlin.getHeight(x+k,z+j))
                if self.td.get((floor(x+k),floor(y),floor(z+j))) ==None:
                    self.genBlock(x+k,y,z+j)
        self.subsets[self.currentSubset].model.generate()
        if self.currentSubset<self.numSubsets-1:
            self.currentSubset+=1
        else:
            self.currentSubset=0
        self.Swirl.move()