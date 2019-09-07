import pyglet
import math
import random

from game import textures
from game import collision
from game import objects
from game import floatingText

class Missile(objects.Object):
    def __init__(self, player, sprite, speed, owner):
        super().__init__()
        self.name = 'missile'
        self.type = 3

        self.moveX = 0
        self.moveY = 0
        self.range = 0
        self.moveTypeX = 0
        self.moveTypeY = 0
        self.sprite = sprite
        self.player = player
        self.activated = False
        self.speedX = 0
        self.speedY = 0
        self.angle = 0
        self.owner = owner
        self.targets = []
        self.damageDealt = False

    def __del__(self):
        self.activated = False
        self.sprite.delete()

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
            
            object = Missile(self.caster.sprite, sprite, self.speed, self.caster.owner)
            self.list.append(object)
            self.manager.missiles.append(object)

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

            self.sound.play()
            object.activated = True
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