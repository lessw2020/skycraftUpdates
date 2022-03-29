from perlin_module import PerlinNoise
'''class Perlin:
    def __init__(self) -> None:
        self.seed=9989
        self.octaves=3
        self.freq=64
        self.amp=12
        
        
        self.pNoise=PerlinNoise(seed=self.seed,octaves=self.octaves)

    def getHeight(self,x,z):
        y=0
        y=self.pNoise([x/self.freq,z/self.freq])*self.amp
        return y
'''
class Perlin:
    def __init__(this):
        
        this.seed = ord('y')+ord('o')
        # Original values.
        this.octaves = 8
        this.freq = 256
        this.amp = 18    

        this.pNoise_continental = PerlinNoise( seed=this.seed,
                                    octaves=1)

        this.pNoise_details = PerlinNoise(  seed=this.seed,
                                    octaves=this.octaves)
        

    def getHeight(this,x,z):
        from math import sin
        y = 0
        y = this.pNoise_continental([x/512,z/512])*128
        y += this.pNoise_details([x/this.freq,z/this.freq])*this.amp
        
        # Apply some predictable surface variation.
        sAmp=0.33
        y+=sin(z)*sAmp
        y+=sin(x*0.5)*sAmp
        return y