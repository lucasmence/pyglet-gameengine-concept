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
