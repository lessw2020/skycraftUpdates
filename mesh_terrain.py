
   
from perlin import Perlin
from ursina import *
from random import random
from infiniteTerrain import swirlEngine
from break_blocks import *
from builder import *
from config import g_sixAxis

class Meshterrain:
    def __init__(this,_sub,_cam):
        
        this.subject = _sub
        this.camera = _cam

        this.block = load_model('block.obj')
        this.textureAtlas = 'texture_atlas_3.png'
        this.numVertices = len(this.block.vertices)

        this.subsets = []
        this.numSubsets = 512
        
        # Must be even number! See genTerrain()
        this.subWidth = 10 
        this.swirlEngine = swirlEngine(this.subWidth)
        this.currentSubset = 0

        # Our terrain dictionary :D
        this.td = {}

        # Our vertex dictionary -- for mining.
        this.vd = {}

        this.perlin = Perlin()

        # Instantiate our subset Entities.
        this.setup_subsets()
    
    def setup_subsets(this):
        ptrAtlas=this.textureAtlas
        for i in range(0,this.numSubsets):
            e = Entity( model=Mesh(),
                        texture=ptrAtlas)
            e.texture_scale*=64/e.texture.width
            this.subsets.append(e)

    def do_mining(this):
        epi = mine(this.td,this.vd,this.subsets)
        if epi != None:
            this.genWalls(epi[0],epi[1])
            this.subsets[epi[1]].model.generate()

    # Highlight looked-at block :)
    # !*!*!*!*!*!*!
    # We don't need to pass in pos and cam anymore?!
    def update(this,pos,cam):
        highlight(pos,cam,this.td)
        # Blister-mining!
        if lookBlock.visible :
            if held_keys['shift'] and held_keys['left mouse']:
                this.do_mining()
            # for key, value in held_keys.items():
            #     if key=='left mouse' and value==1:
            #         this.do_mining()

    def input(this,key):
        if key=='left mouse up' and lookBlock.visible :
            this.do_mining()
        # Building :)
        if key=='right mouse up' and lookBlock.visible :
            bsite = checkBuild( lookBlock.position,this.td,
                                this.camera.forward,
                                this.subject.position+Vec3(0,this.subject.height,0))
            if bsite!=None:
                this.genBlock(floor(bsite.x),floor(bsite.y),floor(bsite.z),subset=0,blockType='grass')
                gapShell(this.td,bsite)
                this.subsets[0].model.generate()
    
    # I.e. after mining, to create illusion of depth.
    def genWalls(this,epi,subset):

        if epi is None: return
        # Refactor this -- place in mining_system 
        # except for cal to genBlock?
        
        for i in range(0,6):
            np = epi + g_sixAxis[i]
            if this.td.get( (floor(np.x),
                            floor(np.y),
                            floor(np.z)))is None:
                this.genBlock(np.x,np.y,np.z,subset,gap=False,blockType='soil')


    def genBlock(this,x,y,z,subset=-1,gap=True,blockType='grass'):
        if subset==-1: subset=this.currentSubset
        # Extend or add to the vertices of our model.
        model = this.subsets[subset].model

        model.vertices.extend([ Vec3(x,y,z) + v for v in 
                                this.block.vertices])
        # Record terrain in dictionary :)
        this.td[(floor(x),floor(y),floor(z))] = 't'
        # Also, record gap above this position to
        # correct for spawning walls after mining.
        if gap:
            key=((floor(x),floor(y+1),floor(z)))
            if this.td.get(key) is None:
                this.td[key]='g'

        # Record subset index and first vertex of this block.
        vob = (subset, len(model.vertices)-37)
        this.vd[(floor(x),
                floor(y),
                floor(z))] = vob

        # Decide random tint for colour of block :)
        c = random()-0.5
        model.colors.extend( (Vec4(1-c,1-c,1-c,1),)*
                                this.numVertices)

        
        # This is the texture atlas co-ord for grass :)
        uu = 8
        uv = 7
        if blockType=='soil':
            uu,uv=g_textureMap.get('soil')

        elif blockType=='stone':
            uu,uv=g_textureMap.get('stone')

        elif blockType=='ice':
            uu,uv=g_textureMap.get('ice')

        # Randomly place stone blocks.
        if y <-30 and random() > 0.86:
            uu,uv=g_textureMap.get('stone')

        # If high enough, cap with snow blocks :D
        if y > 2:
            uu,uv=g_textureMap.get('snow')

        model.uvs.extend([Vec2(uu,uv) + u for u in this.block.uvs])

    def genTerrain(this):
        # Get current position as we swirl around world.
        x = floor(this.swirlEngine.pos.x)
        z = floor(this.swirlEngine.pos.y)

        d = int(this.subWidth*0.5)
        ptrGitHeight=this.perlin.getHeight

        xk=0
        zj=0

        for k in range(-d,d):
            xk=x+k

            for j in range(-d,d):

                zj=z+j

                y = floor(ptrGitHeight(xk,zj))
                if this.td.get( (floor(xk),
                                floor(y),
                                floor(zj)))is None:
                    this.genBlock(xk,y,zj,blockType='grass')

        this.subsets[this.currentSubset].model.generate()
        # Current subset hack ;)
        if this.currentSubset<this.numSubsets-1:
            this.currentSubset+=1
        else: this.currentSubset=0
        this.swirlEngine.move()