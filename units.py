import pyglet
import math
from pyglet.window import key

from game import textures
from game import abilities
from game import attackTypes
from game import collision
from game import objects

class Animation():
    def __init__(self):
        self.time = []
        self.timeMax = []
        self.imageList = []
        self.index = 0
        self.indexCount = 0
        self.sprite = None
    

    def animate(self, sprite, image, timeMax):
        self.sprite = sprite
        self.sprite.image = image[0]
        self.imageList = image
        self.timeMax = timeMax
        self.index = 0
        self.indexCount = len(image) - 1
        self.time = []
        for time in self.timeMax:
            self.time.append(0)

    def update(self, dt):

        result = False

        if self.index <= self.indexCount and len(self.imageList) > 0:
            if self.time[self.index] < self.timeMax[self.index]:
                self.time[self.index] += 1 * dt 
            elif self.index < self.indexCount:
                self.index += 1
                self.sprite.image = self.imageList[self.index]
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

class AnimationManager():
    def __init__(self, sprite):
        self.animationList = []
        self.currentAnimation = ''

        self.animationExecute = Animation()
        self.sprite = sprite

    def animate(self, name):
        if (self.currentAnimation != name):
            for animation in self.animationList:
                if animation.name == name: 
                    self.currentAnimation = name
                    self.animationExecute.animate(self.sprite, animation.sprite, animation.time)
        
    def update(self, dt):
        if self.animationExecute.update(dt) == True:
            self.currentAnimation = ''
            self.animate('stand')
        
class Bonus():
    def __init__(self):
        self.attack = 0
        self.movementSpeed = 0
        self.armor = 0
        self.healthMax = 0
        self.energyMax = 0
        self.healthRegeneration = 0
        self.energyRegeneration = 0
        self.critical = 0
        self.attackSpeed = 0    

class Unit(objects.Object):
    def __init__(self, mainBatch, positionX, positionY, owner, manager):
        super().__init__()
        self.texture = textures.texture_load('game/sprites/ninja-red.png', 1, 2, 100, 100, 0.5, True)
        self.sprite = pyglet.sprite.Sprite(self.texture, x=positionX, y=positionY, batch=mainBatch)
        self.animation = AnimationManager(self.sprite)
        self.specialEffect = False
        self.manager = manager
        self.batch = mainBatch
        self.name = 'unit'
        self.owner = owner
        self.type = 1
        self.attackSpeed = 1
        self.healthMax = 10
        self.health = self.healthMax
        self.healthRegeneration = 0.10
        self.energyMax = 10
        self.energy = self.energyMax 
        self.energyRegeneration = 0.50
        self.armor = 0 
        self.critical = 0.10
        self.bonus = Bonus()
        self.angle = 0
        self.diferenceX = 0
        self.diferenceY = 0
        self.moveX = positionX
        self.moveY = positionY
        self.movementSpeed = 0
        self.minimumRange = 10
        self.bar = Bar(mainBatch, self)
        self.moving = False
        self.skillQ = None
        self.skillW = None
        self.skillE = None
        self.skillR = None
        self.attack = None  
        self.alive = True
        self.paused = False
        self.A = 0
        self.Q = 1
        self.W = 2
        self.E = 3
        self.R = 4
    
    def kill(self):
        if self.specialEffect == False:
            self.bar.sprite.delete()
            del self.bar

        if (self.attack != None):
            for object in self.attack.list:
                object.sprite.delete()
                del object

        if (self.skillQ != None):
            for object in self.skillQ.list:
                object.sprite.delete()
                del object

        if (self.skillW != None):
            for object in self.skillW.list:
                object.sprite.delete()
                del object

        if (self.skillE != None):
            for object in self.skillE.list:
                object.sprite.delete()
                del object

        if (self.skillR != None):
            for object in self.skillR.list:
                object.sprite.delete()
                del object

        self.health = 0
        self.healthRegeneration = 0
        self.energy = 0
        self.energyRegeneration = 0
        self.alive = False   
        self.paused = False
        self.sprite.delete()

    def on_mouse_press(self, x, y, button, modifiers):    
        if (button == 4):  
            self.angle = collision.angle(x, self.sprite.x, y, self.sprite.y)
            self.moveX = x
            self.moveY = y
            
            self.moving = True

        if (button == 1):  
            self.cast(self.A, x, y)

    def on_key_press(self, symbol, modifiers, mouseX, mouseY):    
        if symbol == key.A:
            self.cast(self.A, mouseX, mouseY)
        if symbol == key.Q:
            self.cast(self.Q, mouseX, mouseY)
        if symbol == key.W:
            self.cast(self.W, mouseX, mouseY)
        if symbol == key.E:
            self.cast(self.E, mouseX, mouseY)
        if symbol == key.R:
            self.cast(self.R, mouseX, mouseY)
 
    def cast(self, type, x ,y):
        if (self.alive == True and self.paused == False):
            
            if type == self.A and self.attack != None:
                self.moving = self.attack.cast(x, y, self.attackSpeed)   
            
            elif type == self.Q and self.skillQ != None:       
                self.moving = self.skillQ.cast(x, y)
            
            elif type == self.W and self.skillW != None:       
                self.moving = self.skillW.cast(x, y)
            
            elif type == self.E and self.skillE != None:       
                self.moving = self.skillE.cast(x, y)
            
            elif type == self.R and self.skillR != None:       
                self.moving = self.skillR.cast(x, y)
            
            if (self.moving == False):
                self.moveX = self.sprite.x
                self.moveY = self.sprite.y  

                self.animation.animate('attack')                

    def update(self, dt):  
        if (self.alive == True):
            self.animation.update(dt)
            if (self.attack != None):
                self.attack.loop(dt)
            
            if (self.skillQ != None):
                self.skillQ.loop(dt)
            
            if (self.skillW != None):
                self.skillW.loop(dt)
            
            if (self.skillE != None):
                self.skillE.loop(dt)
            
            if (self.skillR != None):
                self.skillR.loop(dt)

            self.health += (self.healthRegeneration + self.bonus.healthRegeneration) * dt
            self.energy += (self.energyRegeneration + self.bonus.energyRegeneration) * dt

            if (self.health > (self.healthMax + self.bonus.healthMax)):
                self.health = (self.healthMax + self.bonus.healthMax)
            if (self.energy > (self.energyMax + self.bonus.energyMax)):
                self.energy = (self.energyMax + self.bonus.energyMax)

            if self.specialEffect == False:
                self.bar.update(self.health, self.healthMax + self.bonus.healthMax)
            
            if (self.moving == True and self.paused == False):    
                if not (collision.collisionObject(self, self.angle, self.manager)):
                    self.animation.animate('walk') 

                    movementX = self.movementSpeed + self.bonus.movementSpeed
                    movementY = self.movementSpeed + self.bonus.movementSpeed

                    self.diferenceX = self.moveX - self.sprite.x
                    self.diferenceY = self.moveY - self.sprite.y

                    if self.diferenceX < 0:
                        self.diferenceX = self.diferenceX * -1
                    if self.diferenceY < 0:
                        self.diferenceY = self.diferenceY * -1

                    if self.diferenceX > self.diferenceY:
                        movementY = movementY * (self.diferenceY/self.diferenceX)
                    elif self.diferenceX < self.diferenceY:
                        movementX = movementX * (self.diferenceX/self.diferenceY)

                    distance = collision.distance(self.diferenceY, self.diferenceX)
                    if  (distance > self.minimumRange):  
                        if self.sprite.x > self.moveX:
                            self.sprite.x -= movementX * dt   
                        if self.sprite.x < self.moveX:
                            self.sprite.x += movementX * dt  

                        if self.sprite.y > self.moveY:
                            self.sprite.y -= movementY * dt   
                        if self.sprite.y < self.moveY:
                            self.sprite.y += movementY * dt  
                    else:
                        self.moving = False  
                        self.animation.animate('stand')             
                else:
                    self.moving = False
                    self.animation.animate('stand') 

            elif (self.paused == True):
                self.moving = False
                self.moveX = self.sprite.x
                self.moveX = self.sprite.y 

            if (self.health <= 0):
                self.kill()

class NinjaDeathEffect(Unit):
    def __init__(self, mainBatch, positionX, positionY, owner, manager):    
        super().__init__(mainBatch, positionX, positionY, owner, manager)
        self.specialEffect = True
        self.name = 'specialEffect'

        spriteY = 0

        self.animation.animationList.append(AnimationSprite([], [], 'stand'))
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/anska.png').get_region(x=7,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.30)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/anska.png').get_region(x=71,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.30)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/anska.png').get_region(x=135,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.30)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/anska.png').get_region(x=200,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.30)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/anska.png').get_region(x=265,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.30)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/anska.png').get_region(x=328,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(1)

        self.totalTime = 0

        for time in self.animation.animationList[len(self.animation.animationList)-1].time:
            self.totalTime += time 

        self.bar.sprite.delete()
        del self.bar

    def update(self, dt):
        super().update(dt)

        self.totalTime -= dt

        if self.totalTime <= 0:
            self.alive = False

class SkeletonWarriorDeathEffect(Unit):
    def __init__(self, mainBatch, positionX, positionY, owner, manager):    
        super().__init__(mainBatch, positionX, positionY, owner, manager)
        self.specialEffect = True
        self.name = 'specialEffect'

        spriteY = 0

        self.animation.animationList.append(AnimationSprite([], [], 'stand'))
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/skeleton-warrior.png').get_region(x=7,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.30)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/skeleton-warrior.png').get_region(x=71,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.15)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/skeleton-warrior.png').get_region(x=135,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.15)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/skeleton-warrior.png').get_region(x=200,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.15)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/skeleton-warrior.png').get_region(x=265,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.15)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/skeleton-warrior.png').get_region(x=328,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(1)

        self.totalTime = 0

        for time in self.animation.animationList[len(self.animation.animationList)-1].time:
            self.totalTime += time 

        self.bar.sprite.delete()
        del self.bar

    def update(self, dt):
        super().update(dt)

        self.totalTime -= dt

        if self.totalTime <= 0:
            self.alive = False
                  
class Ninja(Unit):
    def __init__(self, mainBatch, positionX, positionY, owner, manager):    
        super().__init__(mainBatch, positionX, positionY, owner, manager)
        
        spriteY = 1090

        self.animation.animationList.append(AnimationSprite([], [], 'stand'))
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/anska.png').get_region(x=6,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.5)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/anska.png').get_region(x=70,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.10)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/anska.png').get_region(x=134,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.10)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/anska.png').get_region(x=198,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.10)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/anska.png').get_region(x=262,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.05)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/anska.png').get_region(x=326,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.05)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/anska.png').get_region(x=390,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.10)

        self.animation.animationList.append(AnimationSprite([], [], 'walk'))
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/anska-move.png').get_region(x=65,y=0,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.05)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/anska-move.png').get_region(x=0,y=0,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.05)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/anska-move.png').get_region(x=130,y=0,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.05)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/anska-move.png').get_region(x=190,y=0,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.05)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/anska-move.png').get_region(x=252,y=0,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.05)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/anska-move.png').get_region(x=315,y=0,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.05)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/anska-move.png').get_region(x=380,y=0,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.05)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/anska-move.png').get_region(x=445,y=0,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.05)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/anska-move.png').get_region(x=510,y=0,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.05)

        self.animation.animationList.append(AnimationSprite([], [], 'attack'))
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/anska-move.png').get_region(x=315,y=0,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.5)

        self.sprite.update(scale=1.00)
        self.name = 'ninja'
        self.attackSpeed = 0.3
        self.healthMax = 50
        self.healthRegeneration = 0.2
        self.energyMax = 10 
        self.armor = 10
        self.movementSpeed = 120
        self.skillQ = abilities.Shuriken(self, self.manager)
        self.attack = attackTypes.Slash(self, self.manager) 
        self.health = self.healthMax + self.bonus.healthMax

    def kill(self):
        if self.name == 'ninja':
            deathEffect = NinjaDeathEffect(self.sprite.batch, self.sprite.x,self.sprite.y, self.owner, self.manager)
            self.manager.specialEffects.append(deathEffect)
        super().kill()


class NinjaMinion(Ninja):  
    def __init__(self, mainBatch, positionX, positionY, owner, manager):    
        super().__init__(mainBatch, positionX, positionY, owner, manager)

        spriteY = 700

        self.animation.animationList.append(AnimationSprite([], [], 'stand'))
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/skeleton-warrior.png').get_region(x=7,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.15)

        self.animation.animationList.append(AnimationSprite([], [], 'walk'))
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/skeleton-warrior.png').get_region(x=7,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.10)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/skeleton-warrior.png').get_region(x=71,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.10)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/skeleton-warrior.png').get_region(x=135,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.10)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/skeleton-warrior.png').get_region(x=200,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.10)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/skeleton-warrior.png').get_region(x=263,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.10)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/skeleton-warrior.png').get_region(x=328,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.10)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/skeleton-warrior.png').get_region(x=392,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.10)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/skeleton-warrior.png').get_region(x=455,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.10)
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/skeleton-warrior.png').get_region(x=520,y=spriteY,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.10)

        self.animation.animationList.append(AnimationSprite([], [], 'attack'))
        self.animation.animationList[len(self.animation.animationList)-1].sprite.append(self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/characters/skeleton-warrior.png').get_region(x=323,y=435,height=50,width=50)], 1, True))
        self.animation.animationList[len(self.animation.animationList)-1].time.append(0.5)


        self.name = 'ninjaMinion'
        self.attackSpeed = 1
        self.healthMax = 10
        self.energyMax = 10 
        self.energyRegeneration = 0.2
        self.healthRegeneration = 0.00
        self.armor = 0
        self.movementSpeed = 50
        self.minimumRange = 50
    
    def update(self, dt):
        self.moving = True
        distance = collision.distance(self.diferenceX, self.diferenceY)
        super().update(dt)

        if (collision.distance(self.diferenceX, self.diferenceY) <= 100):
            self.cast(self.A, self.moveX, self.moveY)  
            
        if (collision.distance(self.diferenceX, self.diferenceY) >= 150):
            self.cast(self.Q, self.moveX, self.moveY)    

    def kill(self):
        deathEffect = SkeletonWarriorDeathEffect(self.sprite.batch, self.sprite.x,self.sprite.y, self.owner, self.manager)
        self.manager.specialEffects.append(deathEffect)
        super().kill()  

class Bar():
    def __init__(self, mainBatch, unit):

        self.texture = pyglet.image.load('game/sprites/healthbar.png')
        self.unit = unit
        self.sprite = pyglet.sprite.Sprite(textures.texture_load('game/sprites/healthbar.png', 1, 1, 0, 100, 1, False), x=unit.sprite.x + unit.sprite.width * 0.20, y=unit.sprite.y + unit.sprite.height, batch=mainBatch, group=pyglet.graphics.OrderedGroup(1))
        self.sprite.update(scale_y = 0.50, scale_x = 0.80)
        self.animation100 = self.sprite.image.from_image_sequence([self.texture.get_region(x=450,y=0,height=15,width=50)], 1, True)
        self.animation090 = self.sprite.image.from_image_sequence([self.texture.get_region(x=400,y=0,height=15,width=50)], 1, True)
        self.animation080 = self.sprite.image.from_image_sequence([self.texture.get_region(x=350,y=0,height=15,width=50)], 1, True)
        self.animation070 = self.sprite.image.from_image_sequence([self.texture.get_region(x=300,y=0,height=15,width=50)], 1, True)
        self.animation060 = self.sprite.image.from_image_sequence([self.texture.get_region(x=250,y=0,height=15,width=50)], 1, True)
        self.animation050 = self.sprite.image.from_image_sequence([self.texture.get_region(x=200,y=0,height=15,width=50)], 1, True)
        self.animation040 = self.sprite.image.from_image_sequence([self.texture.get_region(x=150,y=0,height=15,width=50)], 1, True)
        self.animation030 = self.sprite.image.from_image_sequence([self.texture.get_region(x=100,y=0,height=15,width=50)], 1, True)
        self.animation020 = self.sprite.image.from_image_sequence([self.texture.get_region(x=50,y=0,height=15,width=50)], 1, True)
        self.animation010 = self.sprite.image.from_image_sequence([self.texture.get_region(x=0,y=0,height=15,width=50)], 1, True)

        self.sprite.image = self.animation100

    def update(self, value, valueMax):
        percentage = value / valueMax
        self.sprite.x = self.unit.sprite.x + self.unit.sprite.width * 0.20
        self.sprite.y = self.unit.sprite.y + self.unit.sprite.height
        if percentage > 0.9:
            self.sprite.image = self.animation100 
        elif percentage > 0.8:
            self.sprite.image = self.animation090
        elif percentage > 0.7:
            self.sprite.image = self.animation080
        elif percentage > 0.6:
            self.sprite.image = self.animation070  
        elif percentage > 0.5:
            self.sprite.image = self.animation060 
        elif percentage > 0.4:
            self.sprite.image = self.animation050 
        elif percentage > 0.3:
            self.sprite.image = self.animation040
        elif percentage > 0.2:
            self.sprite.image = self.animation030
        elif percentage > 0.1:
            self.sprite.image = self.animation020  
        elif percentage > 0.0:
            self.sprite.image = self.animation010 




            
        

          