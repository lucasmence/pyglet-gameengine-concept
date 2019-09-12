import pyglet
import math
import random

from game import textures
from game import collision
from game import objects
from game import floatingText
from game import texturePacks
from game import sounds

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
        self.speedX = speed
        self.speedY = speed
        self.speed = speed
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
        self.rotationFirstTime = True

    def __del__(self):
        self.activated = False
        if self.sprite != None:
            self.sprite.delete()
    
    def spawn(self, texture, initialX, initialY, positionX, positionY, scale, list, manager):
        if self.sprite == None:
            self.sprite = pyglet.sprite.Sprite(texture, initialX, initialY, batch=self.caster.batch, group=pyglet.graphics.OrderedGroup(2))
            self.sprite.update(scale=scale)
        
            list.append(self)
            manager.missiles.append(self)

            self.moveX = positionX
            self.moveY = positionY

            self.activated = True

    def moveLinear(self, dt):
        if self.linearEnabled == False:
            self.linearEnabled = True
            diferenceX = self.moveX - self.sprite.x
            diferenceY = self.moveY - self.sprite.y

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

    def moveRotation(self, radius, speed, x, y, modifier):
        if self.rotationEnabled == False:
            self.rotationEnabled = True
            self.rotationIteractions = (int(2 * radius * math.pi) * speed)
            self.rotationSin = math.sin(2* math.pi / self.rotationIteractions)
            self.rotationCos = math.cos(2 * math.pi / self.rotationIteractions) 
            if self.rotationFirstTime == True:
                self.rotationFirstTime = False
                self.rotationIndex = 0 + int(self.rotationIteractions * (modifier / 100))
            else:
                self.rotationIndex = 0
            self.rotationDx, self.rotationDy = radius, 0

        if self.rotationIndex < int(self.rotationIteractions)+1:   
            self.sprite.x = (x + self.rotationDx)
            self.sprite.y = (y + self.rotationDy)
            self.rotationDx, self.rotationDy = (self.rotationDx * self.rotationCos - self.rotationDy * self.rotationSin), (self.rotationDy * self.rotationCos + self.rotationDx * self.rotationSin)
            self.rotationIndex += 1
        else:
            self.rotationEnabled = False

class MissileEnchanter():
    def coneArea(self, missile, count, angle, x, y, list, manager):

        constants = [1, -1]

        for constant in constants:
            midpoint = int(constant * -1)
            if midpoint < 0:
                midpoint = 0
            for index in range(count):
                object = Missile(missile.caster, None, missile.speed)
                object.spawn(missile.sprite.image, missile.sprite.x, missile.sprite.y, x, y, missile.sprite.scale, list, manager)

                object.linearEnabled = True

                diferenceX = x - object.sprite.x
                diferenceY = y - object.sprite.y

                newAngle = (int(angle / count) * (index + midpoint) * constant) * -1
                object.angle = collision.angle(x, object.sprite.x, y, object.sprite.y) + newAngle

                object.sprite.image.anchor_x = object.sprite.width / 2
                object.sprite.image.anchor_y = object.sprite.height / 2

                object.sprite.rotation = object.angle *-1

                if diferenceX < 0:
                    diferenceX = diferenceX * -1
                if diferenceY < 0:
                    diferenceY = diferenceY * -1

                if diferenceX > diferenceY:
                    object.speedY = object.speedY * (diferenceY/diferenceX) + ((6 * int(angle / count))  * (index + midpoint) * constant)
                elif diferenceX < diferenceY:
                    object.speedX = object.speedX * (diferenceX/diferenceY) - ((6 * int(angle / count)) * (index + midpoint) * constant) 
                
                if (object.sprite.x < x):
                    object.moveTypeX = 0
                if (object.sprite.x > x):
                    object.moveTypeX = 1

                if (object.sprite.y < y):
                    object.moveTypeY = 0
                if (object.sprite.y > y):
                    object.moveTypeY = 1      

                object.activated = True    

        list.remove(missile)
        manager.missiles.remove(missile)
        del missile
        
class Skill(objects.Object):
    def __init__(self, caster, manager):
        super().__init__()
        self.manager = manager
        self.caster = caster
        self.id = 0
        self.name = 'skill'
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

        self.missileStartPositionX = int(self.caster.sprite.width / 2)
        self.missileStartPositionY = int(self.caster.sprite.height / 2)
       
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

            if self.sound != None:
                self.sound.play()
            
            return True
        else:
            return False
        
    def loop(self, dt):
        if self.cooldownTime < self.cooldown:    
            self.cooldownTime += dt 

class SkillLinear(Skill):    
    def __init__(self, caster, manager):
        super().__init__(caster, manager)
        self.autoGenerateMissile = True 
            
    def cast(self, x, y):
        activated = super().cast(x, y)
        if activated == True and self.autoGenerateMissile == True:
            object = Missile(self.caster, None, self.speed)
            object.spawn(self.texture, self.caster.sprite.x + self.missileStartPositionX, self.caster.sprite.y + self.missileStartPositionY, x, y, self.scale, self.list, self.manager)
        return activated
        
    def loop(self, dt):
        super().loop(dt)

        for object in self.list:
            if (object.activated == True):

                object.moveLinear(dt)               

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

class SkillDoubleStep(Skill):
    def __init__(self, caster, manager):
        super().__init__(caster, manager)
        self.id = 0
        self.name = 'skillDoubleStep'
        self.step = 0
        self.cooldownStep = [1, 1]
        self.cooldownStepTime = [self.cooldownStep[0], self.cooldownStep[1]]
        self.cooldown = self.cooldownStep[0]
        self.cooldownTime = self.cooldown
        self.castingTimeStep = [0.25, 0.25]
        self.castingTime = self.castingTimeStep[0]
        self.energyStep = [1, 0]
        self.energy = self.energyStep[0]
        self.timeStep = 5
        self.stepFailed = False
       
        self.soundStep = [None, None]
        self.sound = self.soundStep[0]
        self.texture = None

    def cast(self, x, y):
        activated = super().cast(x, y)
        if activated == True:
            self.stepFailed = False
            if self.step == 0:
                self.step = 1
            elif self.step == 1:
                self.step = 0
            self.energy = self.energyStep[self.step]
            self.cooldown = self.cooldownStep[self.step]
            self.castingTime = self.castingTimeStep[self.step]

            if self.sound != None:
                self.sound = self.soundStep[self.step]

        return activated
        
    def loop(self, dt):
        if self.cooldownTime < self.cooldown or self.cooldownTime < self.timeStep:
            self.cooldownTime += dt
        if self.step != 0 and self.cooldownTime >= self.timeStep:
            self.stepFailed = True
            self.step = 0
            self.energy = self.energyStep[self.step]
            self.cooldown = self.cooldownStep[self.step]
            self.cooldownTime = 0
            self.castingTime = self.castingTimeStep[self.step]

class SkillBuff(Skill):
    def __init__(self, caster, manager):
        super().__init__(caster, manager)
        self.id = 0
        self.name = 'skillBuff'
        self.durationMax = 5
        self.duration = 0
        self.activated = False
    
    def destroy(self):
        super().destroy()
        self.duration = self.durationMax
        
    def cast(self, x, y):
        activated = super().cast(x, y)
        if activated == True:
            self.duration = 0
            if self.activated == False:
                self.activated = True
                if self.texture != None:
                    self.sprite = pyglet.sprite.Sprite(self.texture, self.caster.sprite.x + self.missileStartPositionX, self.caster.sprite.y + self.missileStartPositionY, batch=self.caster.batch, group=pyglet.graphics.OrderedGroup(2))
                    self.sprite.update(scale=self.scale)
        return activated
        
    def loop(self, dt):
        super().loop(dt)
        if self.duration < self.durationMax and self.activated == True:
            self.duration += dt
            self.sprite.x = self.caster.sprite.x + self.missileStartPositionX
            self.sprite.y = self.caster.sprite.y + self.missileStartPositionY
        elif self.activated == True:
            self.duration = 0
            self.activated = False
            self.sprite.delete()

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

        soundEnchanter = sounds.SoundEnchanter()
        sound = soundEnchanter.load('shuriken', manager)
        del soundEnchanter
        self.sound = sound.file

        tilesetEnchanter = texturePacks.TilesetEnchanter()
        tileset = tilesetEnchanter.load('shuriken', manager)
        del tilesetEnchanter
        self.texture = tileset.texture    

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
       
        soundEnchanter = sounds.SoundEnchanter()
        sound = soundEnchanter.load('shield', manager)
        del soundEnchanter
        self.sound = sound.file

        tilesetEnchanter = texturePacks.TilesetEnchanter()
        tileset = tilesetEnchanter.load('shield', manager)
        del tilesetEnchanter
        self.texture = tileset.texture
    
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

class SteelStorm(SkillDoubleStep):
    def __init__(self, caster, manager):
        super().__init__(caster, manager)
        self.name = 'steelStorm'
        self.cooldownStep = [10, 2]
        self.cooldownStepTime = [self.cooldownStep[0], self.cooldownStep[1]]
        self.cooldown = self.cooldownStep[0]
        self.cooldownTime = self.cooldown
        self.castingTimeStep = [0.25, 0.00]
        self.castingTime = self.castingTimeStep[0]
        self.energyStep = [5, 0]
        self.energy = self.energyStep[0]
        self.timeStep = 5
        self.damage = 2
        self.shurikenCount = 5
        self.scale = 0.50
        self.rangeMax = 700
        self.speed = 500
        self.wave = False
        self.singleTarget = True
        self.criticalChance = 5

        soundEnchanter = sounds.SoundEnchanter()
        sound = soundEnchanter.load('shuriken', manager)
        del soundEnchanter
        self.soundStep = [sound.file, sound.file]
        self.sound = self.soundStep[0]

        tilesetEnchanter = texturePacks.TilesetEnchanter()
        tileset = tilesetEnchanter.load('shuriken', manager)
        del tilesetEnchanter
        self.texture = tileset.texture

        self.list = []
        
    def cast(self, x, y):
        active = super().cast(x, y)
        if active == True:
            if self.step == 1:
                for index in range(self.shurikenCount):
                    sprite = pyglet.sprite.Sprite(self.texture, self.caster.sprite.x + int(self.caster.sprite.width / 2), self.caster.sprite.y + int(self.caster.sprite.height / 2), batch=self.caster.batch, group=pyglet.graphics.OrderedGroup(2))
                    sprite.update(scale=self.scale)
                    
                    object = Missile(self.caster, sprite, self.speed)
                    object.id = index * 20
                    self.list.append(object)
                    self.manager.missiles.append(object)

                    object.moveX = x
                    object.moveY = y

                    object.activated = True
            elif self.step == 0:
                for object in self.list:
                    if object.activated == True:
                        object.moveX = x
                        object.moveY = y    
        
    def loop(self, dt):
        super().loop(dt)
        
        if len(self.list) == 0 and self.step == 1:
            self.cooldownTime = self.timeStep

        for object in self.list:
            if object.activated == True:
                if self.step == 0: 
                    if self.stepFailed == False:
                        object.moveLinear(dt)
                    else:
                        for object in self.list:
                            object.range = self.rangeMax

                elif self.step == 1:
                    object.moveRotation(70, 0.10, self.caster.sprite.x + int(self.caster.sprite.width / 2), self.caster.sprite.y + int(self.caster.sprite.height / 2), object.id)
                
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
