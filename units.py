import pyglet
import math
from pyglet.window import key

from game import textures
from game import abilities
from game import attackTypes
from game import collision
from game import objects

class Unit(objects.Object):
    def __init__(self, mainBatch, positionX, positionY, owner, manager):
        super().__init__()
        self.texture = textures.texture_load('game/sprites/ninja-red.png', 1, 2, 100, 100, 0.5, True)
        self.sprite = pyglet.sprite.Sprite(self.texture, x=positionX, y=positionY, batch=mainBatch)
        self.animationAttack = None
        self.animationTime = 0
        self.animationAttackTime = 0.30
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
        self.A = 0
        self.Q = 1
        self.W = 2
        self.E = 3
        self.R = 4
    
    def kill(self):
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
        self.sprite.delete()

    def on_mouse_press(self, x, y, button, modifiers):    
        if (button == 4):  
            self.angle = collision.angle(y, self.sprite.y, x, self.sprite.x)
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
        if (self.alive == True):
            
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

                if (self.animationAttack != None):
                    self.sprite.image = self.animationAttack
                    self.animationTime = 0                

    def update(self, dt):
        if (self.alive == True):
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

            self.health += self.healthRegeneration * dt
            self.energy += self.energyRegeneration * dt

            if (self.health > self.healthMax):
                self.health = self.healthMax
            if (self.energy > self.energyMax):
                self.energy = self.energyMax
            
            if self.animationTime > self.animationAttackTime:
                self.animationTime = self.animationAttackTime
                self.sprite.image = self.texture
            else:
                self.animationTime += 1 * dt

            self.bar.update(self.health, self.healthMax)
            
            if (self.moving == True):    
                if not (collision.collisionObject(self, self.angle, self.manager)):
                    movementX = self.movementSpeed
                    movementY = self.movementSpeed

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
                else:
                    self.moving = False
            if (self.health <= 0):
                self.kill()

class Ninja(Unit):
    def __init__(self, mainBatch, positionX, positionY, owner, manager):    
        super().__init__(mainBatch, positionX, positionY, owner, manager)
        self.texture = textures.texture_load('game/sprites/ninja-red.png', 1, 2, 100, 100, 0.5, True)
        self.sprite.image = self.texture
        self.animationAttack = self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/ninja-red.png').get_region(x=200,y=0,height=100,width=100)], 0.5, True)
        self.sprite.update(scale=0.50)
        self.name = 'ninja'
        self.attackSpeed = 0.3
        self.healthMax = 50
        self.health = self.healthMax
        self.healthRegeneration = 0.2
        self.energyMax = 10 
        self.armor = 10
        self.movementSpeed = 120
        self.skillQ = abilities.Shuriken(self, self.manager)
        self.attack = attackTypes.Slash(self, self.manager)  


class NinjaMinion(Ninja):  
    def __init__(self, mainBatch, positionX, positionY, owner, manager):    
        super().__init__(mainBatch, positionX, positionY, owner, manager)
        self.texture = textures.texture_load('game/sprites/ninja-gray.png', 1, 2, 100, 100, 0.5, True)
        self.sprite.image = self.texture
        self.animationAttack = self.sprite.image.from_image_sequence([pyglet.image.load('game/sprites/ninja-gray.png').get_region(x=200,y=0,height=100,width=100)], 0.5, True)
        self.name = 'ninjaMinion'
        self.attackSpeed = 1
        self.healthMax = 10
        self.energyMax = 10 
        self.energyRegeneration = 0.2
        self.healthRegeneration = 0.00
        self.armor = 0
        self.movementSpeed = 50
        self.minimumRange = 100
    
    def update(self, dt):
        self.moving = True
        distance = collision.distance(self.diferenceX, self.diferenceY)
        super().update(dt)

        if (collision.distance(self.diferenceX, self.diferenceY) <= 120):
            self.cast(self.A, self.moveX, self.moveY)  
            
        if (collision.distance(self.diferenceX, self.diferenceY) >= 150):
            self.cast(self.Q, self.moveX, self.moveY) 

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




            
        

          