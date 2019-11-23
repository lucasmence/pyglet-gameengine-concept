import pyglet
import math
import random

from game import textures
from game import collision
from game import objects
from game import floatingText
from game import texturePacks
from game import sounds
from game import damage

class Missile(objects.Object):
    def __init__(self, caster, sprite, speed):
        super().__init__()
        self.name = 'missile'
        self.type = 3
        self.caster = caster

        self.damage = 0
        self.lifesteal = 0
        self.moveX = 0
        self.moveY = 0
        self.range = 0
        self.moveTypeX = 0
        self.moveTypeY = 0
        self.stage = 0
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
        self.situation = 0

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
    
    def updateDirection(self, positionX, positionY):
        self.linearEnabled = False
        self.moveX = positionX
        self.moveY = positionY
        self.speedX = self.speed
        self.speedY = self.speed

    def moveLinear(self, dt):
        if self.linearEnabled == False:
            self.linearEnabled = True
            diferenceX = self.moveX - self.sprite.x
            diferenceY = self.moveY - self.sprite.y

            self.angle = collision.angle(self.moveX, self.sprite.x, self.moveY, self.sprite.y)

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
                object.stage = missile.stage
                object.damage = missile.damage

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
        self.lifesteal = 0
        self.energy = 1
        self.scale = 1
        self.wave = False
        self.singleTarget = True
        self.criticalChance = 5
        self.icon = 'icon-unknown'
        self.title = 'An ability'
        self.description = 'No ability description available.'
        self.attackType = False

        self.missileStartPositionX = int(self.caster.sprite.width / 2)
        self.missileStartPositionY = int(self.caster.sprite.height / 2)
       
        self.sound = None
        self.texture = None
        self.list = []
    
    def destroy(self):
        for object in self.list:
            object.range = self.rangeMax
    
    def getTooltip(self):
        labelSecond = ' seconds'
        if self.cooldown < 2:
            labelSecond = ' second'

        labelCooldown = 'Cooldown: '
        labelEnergy = 'Energy: ' + str(self.energy) + '\u2028'
        if self.attackType == True:
            labelCooldown = 'Attack Speed: '
            labelEnergy = ''

        return self.title + '\u2028' + labelCooldown + str(self.cooldown) + labelSecond + '\u2028' + labelEnergy + self.description
        
    def cast(self, x, y):
        if (self.cooldownTime >= self.cooldown and self.caster.energy >= self.energy):
            self.caster.energy -= self.energy
            self.cooldownTime = 0
            self.caster.pausedTime = self.castingTime
            self.caster.angle = collision.angle(x, self.caster.sprite.x, y, self.caster.sprite.y)

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
            object.damage = self.damage
        return activated
        
    def loop(self, dt):
        super().loop(dt)

        for object in self.list:
            if (object.activated == True):

                if (object.range >= self.rangeMax):
                    self.list.remove(object)
                    self.manager.missiles.remove(object)
                    del object
                else:
                    object.moveLinear(dt)               

                    colideValue = collision.collisionObject(object, object.angle, self.manager)

                    if (colideValue != None):
                        if isinstance(colideValue, int):
                            if colideValue == 1:
                                object.situation = 1
                                object.range = self.rangeMax
                        elif (colideValue.health > 0) and (not colideValue in object.targets):
                            object.situation = 2
                            object.targets.append(colideValue)
                            if self.wave == False:
                                object.range = self.rangeMax
                    
                            if (self.singleTarget == True and object.damageDealt == False) or (self.singleTarget == False):
                                object.damageDealt = True

                                damageValue = damage.Damage(object.damage, self.lifesteal, self.criticalChance, self.caster, colideValue, self.manager)
                                del damageValue

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
        if self.duration < self.durationMax and self.activated == True and self.caster.health > 0:
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

class ShurikenCone(SkillLinear):
    def __init__(self, caster, manager):
        super().__init__(caster, manager)
        self.name = 'shuriken-cone'
        self.cooldown = 0.50
        self.cooldownTime = self.cooldown
        self.rangeMax = 200
        self.speed = 550
        self.damage = 1
        self.lifesteal = 1.25
        self.energy = 2
        self.wave = False
        self.singleTarget = True
        self.castingTime = 0.15
        self.criticalChance = 5
        self.autoGenerateMissile = False
        self.scale = 0.50
        self.icon = 'icon-shuriken'
        self.title = 'Rake'
        self.description = 'Release 4 shurikens at a cone area dealing 1 damage each and restoring 1.25 HP each hit.'

        soundEnchanter = sounds.SoundEnchanter()
        sound = soundEnchanter.load('shuriken', manager)
        del soundEnchanter
        self.sound = sound.file

        tilesetEnchanter = texturePacks.TilesetEnchanter()
        tileset = tilesetEnchanter.load('shuriken', manager)
        del tilesetEnchanter
        self.texture = tileset.texture
 
    def cast(self, x, y):
        result = super().cast(x, y)

        if result == True:
            object = Missile(self.caster, None, self.speed)
            object.spawn(self.texture, self.caster.sprite.x + self.missileStartPositionX, self.caster.sprite.y + self.missileStartPositionY, x, y, self.scale, self.list, self.manager)
            object.damage = self.damage
            object.stage = 2
            missileEnchanter = MissileEnchanter()
            missileEnchanter.coneArea(object, 2, 45, x, y, self.list, self.manager)
            del missileEnchanter

        return result
    
    def loop(self, dt):
        for object in self.list:
            if object.range >= (self.rangeMax * 0.80) and object.stage == 2 and object.situation == 0:
                object.stage = 1
                object.speedX = object.speedX / 10
                object.speedY = object.speedY / 10
            elif object.range >= self.rangeMax and object.stage == 1 and object.situation == 0:
                object.stage = 0
                object.range = self.rangeMax * 0.10
                object.speedX = object.speedX * 10
                object.speedY = object.speedY * 10
                object.updateDirection(self.caster.sprite.x + int(self.caster.sprite.width / 2), self.caster.sprite.y + int(self.caster.sprite.height / 2))

        super().loop(dt)
                            
class ShieldBlock(SkillBuff):
    def __init__(self, caster, manager):
        super().__init__(caster, manager)
        self.name = 'shieldBlock'
        self.cooldown = 12
        self.cooldownTime = self.cooldown 
        self.castingTime = 0.10
        self.durationMax = 5
        self.energy = 3
        self.scale = 1
        self.icon = 'icon-shield-block'
        self.title = 'Power Shield'
        self.description = 'Increase your armor by 50 and your attack by 1 for 5 seconds.'
        
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
            self.caster.bonus.armor = self.caster.bonus.armor + 50
            self.caster.bonus.attack = self.caster.bonus.attack + 1
    
    def loop(self, dt):
        activate = self.activated
        super().loop(dt)
        if activate == True and self.activated == False:
            self.caster.bonus.armor = self.caster.bonus.armor - 50
            self.caster.bonus.attack = self.caster.bonus.attack - 1

class FlameSword(SkillBuff):
    def __init__(self, caster, manager):
        super().__init__(caster, manager)
        self.name = 'flameSword'
        self.cooldown = 30
        self.cooldownTime = self.cooldown 
        self.castingTime = 0.00
        self.durationMax = 10
        self.energy = 5
        self.scale = 1
        self.icon = 'icon-attack-fire'
        self.title = 'Flame Sword'
        self.description = 'Changes your attack type to a fire wave attack that deals 2 damage at linear area and increase your HP regeneration by 1 per second by 10 seconds.'
        
        self.missileStartPositionX = 0
        self.missileStartPositionY = 0
       
        soundEnchanter = sounds.SoundEnchanter()
        sound = soundEnchanter.load('fire', manager)
        del soundEnchanter
        self.sound = sound.file

        tilesetEnchanter = texturePacks.TilesetEnchanter()
        tileset = tilesetEnchanter.load('shield-fire', manager)
        del tilesetEnchanter
        self.texture = tileset.texture
    
    def cast(self, x, y):
        from game import attackTypes

        activate = self.activated
        super().cast(x, y)
        if activate == False and self.activated == True:
            self.attackType = self.caster.attack
            self.caster.bonus.healthRegeneration = self.caster.bonus.healthRegeneration + 1
            self.caster.attack = attackTypes.SlashFire(self.caster, self.manager) 
    
    def loop(self, dt):
        activate = self.activated
        super().loop(dt)
        if activate == True and self.activated == False:
            for object in self.caster.attack.list:
                self.manager.missiles.remove(object)
                del object
            del self.caster.attack

            self.caster.bonus.healthRegeneration = self.caster.bonus.healthRegeneration - 1
            self.caster.attack = self.attackType

class SinisterAura(SkillBuff):
    def __init__(self, caster, manager):
        super().__init__(caster, manager)
        self.name = 'sinisterAura'
        self.cooldown = 4
        self.cooldownTime = self.cooldown 
        self.castingTime = 0.00
        self.durationMax = 2
        self.energy = 4
        self.scale = 1
        self.icon = 'icon-sinister-aura'
        self.title = 'Sinister Aura'
        self.description = 'Increase your movement speed by 100 for 2 seconds.'
        
        self.missileStartPositionX = 0
        self.missileStartPositionY = 0
       
        soundEnchanter = sounds.SoundEnchanter()
        sound = soundEnchanter.load('shield', manager)
        del soundEnchanter
        self.sound = sound.file

        tilesetEnchanter = texturePacks.TilesetEnchanter()
        tileset = tilesetEnchanter.load('shield-orange', manager)
        del tilesetEnchanter
        self.texture = tileset.texture
    
    def cast(self, x, y):
        activate = self.activated
        super().cast(x, y)
        if activate == False and self.activated == True:
            self.caster.bonus.movementSpeed = self.caster.bonus.movementSpeed + 100
    
    def loop(self, dt):
        activate = self.activated
        super().loop(dt)
        if activate == True and self.activated == False:
            self.caster.bonus.movementSpeed = self.caster.bonus.movementSpeed - 100

class SoulArrows(SkillBuff):
    def __init__(self, caster, manager):
        super().__init__(caster, manager)
        self.name = 'sinisterAura'
        self.cooldown = 20
        self.cooldownTime = self.cooldown 
        self.castingTime = 0.00
        self.durationMax = 6
        self.energy = 7
        self.scale = 1
        self.icon = 'icon-fire-soul'
        self.title = 'Soul Arrows'
        self.description = 'Increase your basic attack by 1 and grants 50% lifesteal for 6 seconds.'
        
        self.missileStartPositionX = 0
        self.missileStartPositionY = 0
       
        soundEnchanter = sounds.SoundEnchanter()
        sound = soundEnchanter.load('fire', manager)
        del soundEnchanter
        self.sound = sound.file

        tilesetEnchanter = texturePacks.TilesetEnchanter()
        tileset = tilesetEnchanter.load('shield-fire-soul', manager)
        del tilesetEnchanter
        self.texture = tileset.texture
    
    def cast(self, x, y):
        activate = self.activated
        super().cast(x, y)
        if activate == False and self.activated == True:
            self.caster.bonus.attack = self.caster.bonus.attack + 1
            self.caster.bonus.lifesteal = self.caster.bonus.lifesteal + 0.5
    
    def loop(self, dt):
        activate = self.activated
        super().loop(dt)
        if activate == True and self.activated == False:
            self.caster.bonus.attack = self.caster.bonus.attack - 1
            self.caster.bonus.lifesteal = self.caster.bonus.lifesteal - 0.5

class ArrowVolley(SkillLinear):
    def __init__(self, caster, manager):
        super().__init__(caster, manager)
        self.name = 'arrow-volley'
        self.cooldown = 5
        self.cooldownTime = self.cooldown 
        self.rangeMax = 1000
        self.speed = 300
        self.damage = 1
        self.energy = 5
        self.wave = False
        self.singleTarget = True
        self.castingTime = 0.50
        self.criticalChance = 5
        self.autoGenerateMissile = False
        self.icon = 'icon-arrow-volley'
        self.title = 'Volley'
        self.description = 'Releases a wave of volley of 10 arrows at a large cone area dealing 1 damage each hit.'

        soundEnchanter = sounds.SoundEnchanter()
        sound = soundEnchanter.load('arrow', manager)
        del soundEnchanter
        self.sound = sound.file

        tilesetEnchanter = texturePacks.TilesetEnchanter()
        tileset = tilesetEnchanter.load('arrow-ranger', manager)
        del tilesetEnchanter
        self.texture = tileset.texture

        self.scale = 1
    
    def cast(self, x, y):
        result = super().cast(x, y)

        if result == True:
            object = Missile(self.caster, None, self.speed)
            object.spawn(self.texture, self.caster.sprite.x + self.missileStartPositionX, self.caster.sprite.y + self.missileStartPositionY, x, y, self.scale, self.list, self.manager)
            object.damage = self.damage
            missileEnchanter = MissileEnchanter()
            missileEnchanter.coneArea(object, 5, 15, x, y, self.list, self.manager)
            del missileEnchanter

        return result

class Shockwave(SkillLinear):
    def __init__(self, caster, manager):
        super().__init__(caster, manager)

        self.name = 'shuriken'
        self.cooldown = 15
        self.cooldownTime = self.cooldown
        self.rangeMax = 1000
        self.speed = 175
        self.damage = 8
        self.energy = 10
        self.scale = 1
        self.wave = True
        self.singleTarget = False
        self.icon = 'icon-shockwave'
        self.title = 'Shockwave'
        self.description = 'Sends a linear wave that deals 8 damage to each enemy unit.'

        soundEnchanter = sounds.SoundEnchanter()
        sound = soundEnchanter.load('shockwave', manager)
        del soundEnchanter
        self.sound = sound.file

        tilesetEnchanter = texturePacks.TilesetEnchanter()
        tileset = tilesetEnchanter.load('slash-shockwave', manager)
        del tilesetEnchanter
        self.texture = tileset.texture    

class BlackShield(SkillBuff):
    def __init__(self, caster, manager):
        super().__init__(caster, manager)
        self.name = 'blackShield'
        self.cooldown = 5
        self.cooldownTime = self.cooldown 
        self.castingTime = 0
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
        tileset = tilesetEnchanter.load('shield-red', manager)
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
        self.cooldownStep = [20, 2]
        self.cooldownStepTime = [self.cooldownStep[0], self.cooldownStep[1]]
        self.cooldown = self.cooldownStep[0]
        self.cooldownTime = self.cooldown
        self.castingTimeStep = [0.25, 0.00]
        self.castingTime = self.castingTimeStep[0]
        self.energyStep = [5, 0]
        self.energy = self.energyStep[0]
        self.timeStep = 7
        self.damage = 3
        self.damageLinear = 2
        self.shurikenCount = 5
        self.scale = 0.50
        self.rangeMax = 500
        self.speed = 500
        self.wave = False
        self.singleTarget = True
        self.criticalChance = 5
        self.icon = 'icon-steel-storm'
        self.title = 'Steelstorm'
        self.description = 'Summon 5 shuriken to turn around this unit dealing 3 damage each hit. '\
                           'After a short time it can be reactivated to release into a linear area dealing 2 damage each hit.'

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
                        object.damage = self.damageLinear
                        object.moveLinear(dt)
                    else:
                        for object in self.list:
                            object.range = self.rangeMax

                elif self.step == 1:
                    object.damage = self.damage
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
                            
                            damageValue = damage.Damage(object.damage, object.lifesteal, self.criticalChance, self.caster, colideValue, self.manager)
                            del damageValue

                if (object.range >= self.rangeMax):
                    self.list.remove(object)
                    self.manager.missiles.remove(object)
                    del object
