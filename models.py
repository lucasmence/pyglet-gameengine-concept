import pyglet
from game import texturePacks
from game import textures
from game import units

class Animation():
    def __init__(self):
        self.time = []
        self.texturePack = None
        self.index = 0
        self.indexCount = 0
        self.sprite = None
    

    def animate(self, sprite, texturePack, name):

        if texturePack != None:
            self.sprite = sprite
            self.texturePack = texturePack.textureFiles[name]
            self.time.clear()
            
            for textureData in self.texturePack:
                self.time.append(0)

            self.index = 0
            self.indexCount = len(self.texturePack) - 1

    def update(self, dt):

        result = False

        if self.texturePack != None:

            if self.index <= self.indexCount and len(self.texturePack) > 0:
                
                if self.time[self.index] < self.texturePack[self.index].time:
                    self.time[self.index] += 1 * dt 
                elif self.index < self.indexCount:
                    self.index += 1
                    self.sprite.image = self.texturePack[self.index].sprite

                else:
                    result = True
            else:
                result = True

        return result

class AnimationSprite():
    def __init__(self, sprite, time, name):
        self.sprite = sprite
        self.time = time
        self.name = name

class Model():
    def __init__(self, sprite):
        self.animationList = []
        self.texturePack = None
        self.currentAnimation = ''

        self.animation = Animation()
        self.sprite = sprite

        self.name = ''
    
    def load(self, name, animation, manager):
        self.name = name

        self.texturePack = None

        for textures in manager.texturePacks:
            if textures.textureName == name:
                self.texturePack = textures
        
        if self.texturePack == None:
            self.texturePack = texturePacks.TexturePack(name)
            self.texturePack.load(self.sprite)
            manager.texturePacks.append(self.texturePack)

        if animation == '':
            animation = 'stand'
        
        self.animate(animation, 0)

    def animate(self, name, angle):

        if (name != 'stand') and (name != 'death'):
            if self.texturePack.leftRightOnly == True:
                if ((angle >= 0) and (angle <= 90)) or ((angle > 270) and (angle <= 360)):
                    name = name + '-right'
                elif (angle > 90) and (angle <= 270):
                    name = name + '-left'    
            else:
                if ((angle >= 0) and (angle <= 60)) or ((angle > 300) and (angle <= 360)):
                    name = name + '-right'
                elif (angle > 60) and (angle <= 120):
                    name = name + '-up'
                elif (angle > 90) and (angle <= 240):
                    name = name + '-left'    
                elif (angle > 240) and (angle <= 300):
                    name = name + '-down'    

        if (self.currentAnimation != name): 
            self.currentAnimation = name
            
            self.animation.animate(self.sprite, self.texturePack, name)
                    
        
    def update(self, dt):
        if self.animation.update(dt) == True and self.texturePack != None:
            self.currentAnimation = ''
            self.animate('stand', 0)
     