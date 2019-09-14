import pyglet
import math
from pyglet.window import key

from game import textures
from game import collision
from game import objects
from game import models
        
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
        self.texture = textures.texture_load('game/sprites/dummy.png', 1, 2, 50, 50, 0.5, True)
        self.sprite = pyglet.sprite.Sprite(self.texture, x=positionX, y=positionY, batch=mainBatch)
        self.model = models.Model(self.sprite)
        self.specialEffect = False
        self.pausedTime = 0.00
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
        self.deathAnimation = True
        self.A = 0
        self.Q = 1
        self.W = 2
        self.E = 3
        self.R = 4
        self.icon = 'icon-unit-unknown'
    
    def kill(self):
        if self.deathAnimation == True:
            deathEffect = DeathAnimation(self.sprite.batch, self.sprite.x,self.sprite.y, self.owner, self.manager, self.model.name)
            self.manager.specialEffects.append(deathEffect)

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
                self.moving = not self.attack.cast(x, y, self.attackSpeed)   
            
            elif type == self.Q and self.skillQ != None:       
                self.moving = not self.skillQ.cast(x, y)
            
            elif type == self.W and self.skillW != None:       
                self.moving = not self.skillW.cast(x, y)
            
            elif type == self.E and self.skillE != None:       
                self.moving = not self.skillE.cast(x, y)
            
            elif type == self.R and self.skillR != None:       
                self.moving = not self.skillR.cast(x, y)
            
            if (self.moving == False):
                self.moveX = self.sprite.x
                self.moveY = self.sprite.y  

                self.model.animate('attack', self.angle)                

    def update(self, dt): 

        if (self.alive == True):

            if self.pausedTime > 0:
                self.paused = True
                self.pausedTime -= dt
            else:
                self.pausedTime = 0
                self.paused = False

            self.model.update(dt)

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
                    self.model.animate('walk', self.angle) 

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
                        self.model.animate('stand', self.angle)             
                else:
                    self.moving = False
                    self.model.animate('stand', self.angle) 

            elif (self.paused == True):
                self.moving = False
                self.moveX = self.sprite.x
                self.moveX = self.sprite.y 

            if (self.health <= 0):
                self.kill()

class DeathAnimation(Unit):
    def __init__(self, mainBatch, positionX, positionY, owner, manager, texture):    
        super().__init__(mainBatch, positionX, positionY, owner, manager)
        self.deathAnimation = False
        self.specialEffect = True
        self.name = 'specialEffect'
        self.totalTime = 0

        self.model.load(texture, 'death', manager)
        self.sprite.image = self.model.texturePack.textureFiles['death'][0].sprite

        for animation in self.model.texturePack.textureFiles['death']:
            self.totalTime += animation.time 
        
        self.bar.sprite.delete()
        del self.bar

    def update(self, dt):
        super().update(dt)

        self.totalTime -= dt

        if self.totalTime <= 0:
            self.alive = False   

class Bar():
    def __init__(self, mainBatch, unit):

        self.texture = pyglet.image.load('game/sprites/hud/healthbar.png')
        self.unit = unit
        self.sprite = pyglet.sprite.Sprite(textures.texture_load('game/sprites/hud/healthbar.png', 1, 1, 0, 100, 1, False), x=unit.sprite.x + unit.sprite.width * 0.20, y=unit.sprite.y + unit.sprite.height, batch=mainBatch, group=pyglet.graphics.OrderedGroup(2))
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




            
        

          