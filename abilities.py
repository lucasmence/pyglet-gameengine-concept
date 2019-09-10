import pyglet
import math
import random

from game import textures
from game import collision
from game import objects
from game import floatingText

class Missile(objects.Object):
    def __init__(self, caster, sprite, speed):
        super().__init__()
        self.name = 'missile'
        self.type = 3
        self.caster = caster

        self.moveX = 0
        self.moveY = 0
        self.range = 0
        self.moveTypeX = 0
        self.moveTypeY = 0
        self.sprite = sprite
        self.player = self.caster.sprite
        self.activated = False
        self.speedX = 0
        self.speedY = 0
        self.angle = 0
        self.owner = self.caster.owner
        self.targets = []
        self.damageDealt = False
        self.linearEnabled = False

        self.rotationSin = 0
        self.rotationCos = 0
        self.rotationDx = 0
        self.rotationDy = 0
        self.rotationIteractions = 0
        self.rotationIndex = 0
        self.rotationEnabled = False

    def __del__(self):
        self.activated = False
        self.sprite.delete()

    def moveLinear(self, dt):
        if self.linearEnabled == False:
            diferenceX = self.moveX - self.sprite.x
            diferenceY = self.moveY - self.sprite.y
            print(self.moveX)

            self.angle = collision.angle(self.moveX, self.sprite.x, self.moveY, self.sprite.y)

            self.caster.angle = collision.angle(self.moveX, self.sprite.x, self.moveY, self.sprite.y)

            self.sprite.image.anchor_x = self.sprite.width / 2
            self.sprite.image.anchor_y = self.sprite.height / 2

            self.sprite.rotation = self.angle *-1

            if diferenceX < 0:
                diferenceX = diferenceX * -1
            if diferenceY < 0:
                diferenceY = diferenceY * -1

            if diferenceX > diferenceY:
                self.speedY = self.speedY * (diferenceY/diferenceX)
            elif diferenceX < diferenceY:
                self.speedX = self.speedX * (diferenceX/diferenceY)
            
            if (self.sprite.x < self.moveX):
                self.moveTypeX = 0
            if (self.sprite.x > self.moveX):
                self.moveTypeX = 1

            if (self.sprite.y < self.moveY):
                self.moveTypeY = 0
            if (self.sprite.y > self.moveY):
                self.moveTypeY = 1 
        else:
            if self.moveTypeX == 1:
                self.sprite.x -= self.speedX * dt      
            else:
                self.sprite.x += self.speedX * dt  

            if self.moveTypeY == 1:
                self.sprite.y -= self.speedY * dt 
            else:
                self.sprite.y += self.speedY * dt 

            distanceX = (self.speedX * dt)
            distanceY = (self.speedY * dt)

            self.range += math.sqrt( ( distanceY * distanceY ) + ( distanceX  * distanceX ) )

    def moveRotation(self, radius, speed, x, y):
        if self.rotationEnabled == False:
            self.rotationEnabled = True
            self.rotationIteractions = int(2 * radius * math.pi) * speed
            self.rotationSin = math.sin(2* math.pi / self.rotationIteractions)
            self.rotationCos = math.cos(2 * math.pi / self.rotationIteractions) 
            self.rotationIndex = 0
            self.rotationDx, self.rotationDy = radius, 0

        if self.rotationIndex < int(self.rotationIteractions)+1:   
            self.sprite.x = (x + self.rotationDx)
            self.sprite.y = (y + self.rotationDy)
            self.rotationDx, self.rotationDy = (self.rotationDx * self.rotationCos - self.rotationDy * self.rotationSin), (self.rotationDy * self.rotationCos + self.rotationDx * self.rotationSin)
            self.rotationIndex += 1
        else:
            self.rotationEnabled = False

class SkillLinear(objects.Object):
    def __init__(self, caster, manager):
        super().__init__()
        self.manager = manager
        self.caster = caster
        self.id = 0
        self.name = 'skillLinear'
        self.cooldown = 1
        self.cooldownTime = self.cooldown 
        self.castingTime = 0.25
        self.rangeMax = 500
        self.speed = 500
        self.damage = 1
        self.energy = 1
        self.scale = 1
        self.wave = False
        self.singleTarget = True
        self.criticalChance = 5

        self.missileStartPositionX = 25
        self.missileStartPositionY = 25
       
        self.sound = None
        self.texture = None
        self.list = []
    
    def destroy(self):
        for object in self.list:
            object.range = self.rangeMax
        
    def cast(self, x, y):
        if (self.cooldownTime >= self.cooldown and self.caster.energy >= self.energy):
            self.caster.energy -= self.energy
            self.cooldownTime = 0
            self.caster.pausedTime = self.castingTime

            sprite = pyglet.sprite.Sprite(self.texture, self.caster.sprite.x + self.missileStartPositionX, self.caster.sprite.y + self.missileStartPositionY, batch=self.caster.batch, group=pyglet.graphics.OrderedGroup(2))
            sprite.update(scale=self.scale)
            
            object = Missile(self.caster, sprite, self.speed)
            self.list.append(object)
            self.manager.missiles.append(object)

            object.moveX = x
            object.moveY = y

            object.speedX = self.speed
            object.speedY = self.speed

            diferenceX = x - object.sprite.x
            diferenceY = y - object.sprite.y

            object.angle = collision.angle(x, object.sprite.x, y, object.sprite.y)

            self.caster.angle = collision.angle(x, object.sprite.x, y, object.sprite.y)

            sprite.image.anchor_x = sprite.width / 2
            sprite.image.anchor_y = sprite.height / 2

            sprite.rotation = object.angle *-1

            if diferenceX < 0:
                diferenceX = diferenceX * -1
            if diferenceY < 0:
                diferenceY = diferenceY * -1

            if diferenceX > diferenceY:
                object.speedY = object.speedY * (diferenceY/diferenceX)
            elif diferenceX < diferenceY:
                object.speedX = object.speedX * (diferenceX/diferenceY)
            
            if (object.sprite.x < x):
                object.moveTypeX = 0
            if (object.sprite.x > x):
                object.moveTypeX = 1

            if (object.sprite.y < y):
                object.moveTypeY = 0
            if (object.sprite.y > y):
                object.moveTypeY = 1   

            object.activated = True
            self.sound.play()
            
            return False
        else:
            return True
        
    def loop(self, dt):
        for object in self.list:
            if (object.activated == True):

                if object.moveTypeX == 1:
                    object.sprite.x -= object.speedX * dt      
                else:
                    object.sprite.x += object.speedX * dt  
                
                if object.moveTypeY == 1:
                    object.sprite.y -= object.speedY * dt 
                else:
                    object.sprite.y += object.speedY * dt 

                distanceX = (object.speedX * dt)
                distanceY = (object.speedY * dt)

                object.range += math.sqrt( ( distanceY * distanceY ) + ( distanceX  * distanceX ) )
                

                object.moveRotation(50, 0.10, self.caster.sprite.x + self.missileStartPositionX, self.caster.sprite.y + self.missileStartPositionY)

                colideValue = collision.collisionObject(object, object.angle, self.manager)

                if (colideValue != None):
                    if isinstance(colideValue, int):
                        if colideValue == 1:
                            object.range = self.rangeMax
                    elif (colideValue.health > 0) and (not colideValue in object.targets):
                        object.targets.append(colideValue)
                        if self.wave == False:
                            object.range = self.rangeMax
                        
                        if (self.singleTarget == True and object.damageDealt == False) or (self.singleTarget == False):
                            object.damageDealt = True
                            
                            damageValue = self.damage * (1 - ((colideValue.armor + colideValue.bonus.armor)/ 100))

                            criticalValue = random.randint(1,100)
                            critical = False
                            if criticalValue <= self.criticalChance:
                                critical = True
                                damageValue = damageValue * 2

                            colideValue.health -= damageValue

                            useCurrentText = False
                            if damageValue > 0.5:
                                for objectText in self.manager.floatingTexts:
                                    if objectText.unit == colideValue and objectText.valueType == 0 and objectText.opacity < 50 and objectText.critical == False:
                                        useCurrentText = True
                                        objectText.value = objectText.value + damageValue
                                        objectText.opacity = 0
                                        objectText.text.y = objectText.unit.sprite.y
                                if useCurrentText == False:
                                    textDamage = floatingText.FloatingText(self.caster.batch, colideValue, damageValue, 0, critical)
                                    self.manager.floatingTexts.append(textDamage)


                if (object.range >= self.rangeMax):
                    self.list.remove(object)
                    self.manager.missiles.remove(object)
                    del object
            
        self.cooldownTime += dt 

class SkillBuff(objects.Object):
    def __init__(self, caster, manager):
        super().__init__()
        self.manager = manager
        self.caster = caster
        self.id = 0
        self.name = 'skillBuff'
        self.cooldown = 1
        self.cooldownTime = self.cooldown 
        self.castingTime = 0.25
        self.durationMax = 5
        self.duration = 0
        self.energy = 1
        self.scale = 1
        self.activated = False
        self.list = []
        
        self.missileStartPositionX = 0
        self.missileStartPositionY = 0
       
        self.sound = None
        self.texture = None
        self.sprite = None
    
    def destroy(self):
        self.duration = self.durationMax
        
    def cast(self, x, y):
        if (self.cooldownTime >= self.cooldown and self.caster.energy >= self.energy):
            self.caster.energy -= self.energy
            self.cooldownTime = 0
            self.caster.pausedTime = self.castingTime

            self.duration = 0
            if self.activated == False:
                self.activated = True
                if self.texture != None:
                    self.sprite = pyglet.sprite.Sprite(self.texture, self.caster.sprite.x + self.missileStartPositionX, self.caster.sprite.y + self.missileStartPositionY, batch=self.caster.batch, group=pyglet.graphics.OrderedGroup(2))
                    self.sprite.update(scale=self.scale)
                
            self.sound.play()

            return False
        else:
            return True
        
    def loop(self, dt):
        if self.duration < self.durationMax and self.activated == True:
            self.duration += dt
            self.sprite.x = self.caster.sprite.x + self.missileStartPositionX
            self.sprite.y = self.caster.sprite.y + self.missileStartPositionY
        elif self.activated == True:
            self.duration = 0
            self.activated = False
            self.sprite.delete()
            
        self.cooldownTime += dt 


class Shuriken(SkillLinear):
    def __init__(self, caster, manager):
        super().__init__(caster, manager)

        self.name = 'shuriken'
        self.cooldown = 2
        self.cooldownTime = self.cooldown
        self.rangeMax = 700
        self.speed = 500
        self.damage = 3
        self.energy = 2
        self.scale = 0.50
       
        self.sound = pyglet.media.load('game/sounds/shuriken.wav', streaming=False) 
        self.texture = textures.texture_load('game/sprites/ninja-shuriken-25x.png', 1, 4, 25, 25, 0.02, True)

class ShieldBlock(SkillBuff):
    def __init__(self, caster, manager):
        super().__init__(caster, manager)
        self.name = 'shieldBlock'
        self.cooldown = 5
        self.cooldownTime = self.cooldown 
        self.castingTime = 0.10
        self.durationMax = 3
        self.energy = 3
        self.scale = 1
        
        self.missileStartPositionX = 0
        self.missileStartPositionY = 0
       
        self.sound = pyglet.media.load('game/sounds/shield.wav', streaming=False) 
        self.texture = pyglet.image.load('game/sprites/characters/shield.png')
    
    def cast(self, x, y):
        activate = self.activated
        super().cast(x, y)
        if activate == False and self.activated == True:
            self.caster.bonus.armor = self.caster.bonus.armor + 100
    
    def loop(self, dt):
        activate = self.activated
        super().loop(dt)
        if activate == True and self.activated == False:
            self.caster.bonus.armor = self.caster.bonus.armor - 100
