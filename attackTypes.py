import pyglet
import math

from game import textures
from game import abilities
from game import collision
from game import texturePacks
from game import sounds

class Attack(abilities.SkillLinear):
    def __init__(self, caster, manager):
        super().__init__(caster, manager)
        self.name = 'attack'
        self.cooldown = 0.5
        self.rangeMax = 50
        self.speed = 500
        self.damage = 1
        self.energy = 0
        self.wave = True
        self.singleTarget = True
        self.castingTime = 0.50
        self.criticalChance = 10
        self.icon = 'icon-attack'
        self.sound = None
        self.texture = None
        self.scale = 1
        self.attackType = True
        
    def cast(self, x, y, attackSpeed):
        if self.cooldown < attackSpeed:
            self.cooldown = attackSpeed
        activated = super().cast(x, y)
        if activated == True and len(self.list) > 0:
            self.list[len(self.list)-1].damage = self.damage + self.caster.bonus.attack
        return activated

class Slash(Attack):
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
        self.icon = 'icon-attack'
        self.scale = 0.75
        self.title = 'Slash'
        self.description = 'Deal 1 damage each hit.'

        soundEnchanter = sounds.SoundEnchanter()
        sound = soundEnchanter.load('slash', manager)
        del soundEnchanter
        self.sound = sound.file

        tilesetEnchanter = texturePacks.TilesetEnchanter()
        tileset = tilesetEnchanter.load('slash', manager)
        del tilesetEnchanter
        self.texture = tileset.texture 
    
    def getTooltip(self):
        self.description = 'Deal ' + str(self.damage) + ' damage each hit.'
        return super().getTooltip()

class Arrow(Attack):
    def __init__(self, caster, manager):
        super().__init__(caster, manager)
        self.name = 'arrow'
        self.cooldown = 1.5
        self.rangeMax = 500
        self.speed = 500
        self.damage = 2
        self.energy = 0
        self.wave = False
        self.singleTarget = True
        self.castingTime = 0.50
        self.criticalChance = 15
        self.scale = 1

        soundEnchanter = sounds.SoundEnchanter()
        sound = soundEnchanter.load('arrow', manager)
        del soundEnchanter
        self.sound = sound.file

        tilesetEnchanter = texturePacks.TilesetEnchanter()
        tileset = tilesetEnchanter.load('arrow', manager)
        del tilesetEnchanter
        self.texture = tileset.texture

class ArrowCone(Attack):
    def __init__(self, caster, manager):
        super().__init__(caster, manager)
        self.name = 'arrow-cone'
        self.cooldown = 2.50
        self.rangeMax = 400
        self.speed = 400
        self.damage = 1
        self.energy = 0
        self.wave = False
        self.singleTarget = True
        self.castingTime = 0.50
        self.criticalChance = 5
        self.autoGenerateMissile = False

        soundEnchanter = sounds.SoundEnchanter()
        sound = soundEnchanter.load('arrow', manager)
        del soundEnchanter
        self.sound = sound.file

        tilesetEnchanter = texturePacks.TilesetEnchanter()
        tileset = tilesetEnchanter.load('arrow', manager)
        del tilesetEnchanter
        self.texture = tileset.texture

        self.scale = 1
       
    def cast(self, x, y, attackSpeed):
        result = super().cast(x, y, attackSpeed)

        if result == True:
            object = abilities.Missile(self.caster, None, self.speed)
            object.spawn(self.texture, self.caster.sprite.x + self.missileStartPositionX, self.caster.sprite.y + self.missileStartPositionY, x, y, self.scale, self.list, self.manager)
            missileEnchanter = abilities.MissileEnchanter()
            missileEnchanter.coneArea(object, 4, 30, x, y, self.list, self.manager)
            del missileEnchanter

        return result
            
