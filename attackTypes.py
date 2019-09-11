import pyglet
import math

from game import textures
from game import abilities
from game import collision
from game import abilities

class Slash(abilities.SkillLinear):
    def __init__(self, caster, manager):
        super().__init__(caster, manager)
        self.name = 'slash'
        self.cooldown = 0.5
        self.rangeMax = 50
        self.speed = 500
        self.damage = 1
        self.energy = 0
        self.wave = True
        self.singleTarget = True
        self.castingTime = 0.50
        self.criticalChance = 10

        self.missileStartPositionX = 25
        self.missileStartPositionY = 25

        self.sound = pyglet.media.load('game/sounds/slash.wav', streaming=False) 
        self.texture = pyglet.image.load('game/sprites/characters/slash.png')
        self.scale = 0.75

        
    def cast(self, x, y, attackSpeed):
        if self.cooldown < attackSpeed:
            self.cooldown = attackSpeed
        return super().cast(x, y)

class Arrow(abilities.SkillLinear):
    def __init__(self, caster, manager):
        super().__init__(caster, manager)
        self.name = 'slash'
        self.cooldown = 1.5
        self.rangeMax = 500
        self.speed = 500
        self.damage = 2
        self.energy = 0
        self.wave = False
        self.singleTarget = True
        self.castingTime = 0.50
        self.criticalChance = 15

        self.missileStartPositionX = 25
        self.missileStartPositionY = 25

        self.sound = pyglet.media.load('game/sounds/arrow.wav', streaming=False) 
        self.texture = pyglet.image.load('game/sprites/characters/arrow.png')
        self.scale = 1

        
    def cast(self, x, y, attackSpeed):
        if self.cooldown < attackSpeed:
            self.cooldown = attackSpeed
        
        return super().cast(x, y)

class ArrowCone(abilities.SkillLinear):
    def __init__(self, caster, manager):
        super().__init__(caster, manager)
        self.name = 'slash'
        self.cooldown = 2.50
        self.rangeMax = 400
        self.speed = 400
        self.damage = 1
        self.energy = 0
        self.wave = False
        self.singleTarget = True
        self.castingTime = 0.50
        self.criticalChance = 5

        self.missileStartPositionX = 25
        self.missileStartPositionY = 25

        self.sound = pyglet.media.load('game/sounds/arrow.wav', streaming=False) 
        self.texture = pyglet.image.load('game/sprites/characters/arrow.png')
        self.scale = 1

        
    def cast(self, x, y, attackSpeed):
        if self.cooldown < attackSpeed:
            self.cooldown = attackSpeed
        
        result = super().cast(x, y)
        if result == True:
            
            x1 = x  
            y1 = y

            for index in range(5):

                sprite = pyglet.sprite.Sprite(self.texture, self.caster.sprite.x + self.missileStartPositionX, self.caster.sprite.y + self.missileStartPositionY, batch=self.caster.batch, group=pyglet.graphics.OrderedGroup(2))
                sprite.update(scale=self.scale)
                
                object = abilities.Missile(self.caster, sprite, self.speed)
                self.list.append(object)
                self.manager.missiles.append(object)
                object.linearEnabled = True

                object.speedX = self.speed
                object.speedY = self.speed

                diferenceX = x1 - object.sprite.x
                diferenceY = y1 - object.sprite.y

                newAngle = 6 * index
                #if object.angle > 90:
                newAngle = newAngle * -1
                object.angle = collision.angle(x1, object.sprite.x, y1, object.sprite.y) + newAngle

                sprite.image.anchor_x = sprite.width / 2
                sprite.image.anchor_y = sprite.height / 2

                sprite.rotation = object.angle *-1

                if diferenceX < 0:
                    diferenceX = diferenceX * -1
                if diferenceY < 0:
                    diferenceY = diferenceY * -1

                if diferenceX > diferenceY:
                    object.speedY = object.speedY * (diferenceY/diferenceX) + 36 * index
                elif diferenceX < diferenceY:
                    object.speedX = object.speedX * (diferenceX/diferenceY) - 36 * index
                
                if (object.sprite.x < x1):
                    object.moveTypeX = 0
                if (object.sprite.x > x1):
                    object.moveTypeX = 1

                if (object.sprite.y < y1):
                    object.moveTypeY = 0
                if (object.sprite.y > y1):
                    object.moveTypeY = 1      

                object.activated = True    
            
            for index in range(5):

                sprite = pyglet.sprite.Sprite(self.texture, self.caster.sprite.x + self.missileStartPositionX, self.caster.sprite.y + self.missileStartPositionY, batch=self.caster.batch, group=pyglet.graphics.OrderedGroup(2))
                sprite.update(scale=self.scale)
                
                object = abilities.Missile(self.caster, sprite, self.speed)
                self.list.append(object)
                self.manager.missiles.append(object)
                object.linearEnabled = True

                object.speedX = self.speed
                object.speedY = self.speed

                diferenceX = x1 - object.sprite.x
                diferenceY = y1 - object.sprite.y

                newAngle = -6 * index
                #if object.angle > 90:
                newAngle = newAngle * -1
                object.angle = collision.angle(x1, object.sprite.x, y1, object.sprite.y) + newAngle

                sprite.image.anchor_x = sprite.width / 2
                sprite.image.anchor_y = sprite.height / 2

                sprite.rotation = object.angle *-1

                if diferenceX < 0:
                    diferenceX = diferenceX * -1
                if diferenceY < 0:
                    diferenceY = diferenceY * -1

                if diferenceX > diferenceY:
                    object.speedY = object.speedY * (diferenceY/diferenceX) - 36 * index
                elif diferenceX < diferenceY:
                    object.speedX = object.speedX * (diferenceX/diferenceY) + 36 * index
                
                if (object.sprite.x < x1):
                    object.moveTypeX = 0
                if (object.sprite.x > x1):
                    object.moveTypeX = 1

                if (object.sprite.y < y1):
                    object.moveTypeY = 0
                if (object.sprite.y > y1):
                    object.moveTypeY = 1      

                object.activated = True    

        return result
