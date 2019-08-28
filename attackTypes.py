import pyglet
import math

from game import textures
from game import abilities
from game import collision
from game import abilities

class Slash(abilities.Shuriken):
    def __init__(self, caster, objectList):
        super().__init__(caster, objectList)
        self.name = 'slash'
        self.cooldown = 0.3
        self.rangeMax = 50
        self.speed = 500
        self.damage = 1
        self.energy = 0

        self.missileStartPositionX = 25
        self.missileStartPositionY = 25

        self.sound = pyglet.media.load('game/sounds/slash.wav', streaming=False) 
        self.texture = pyglet.image.load('game/sprites/characters/slash.png')
        self.scale = 0.75

        
    def cast(self, x, y, attackSpeed):
        if self.cooldown < attackSpeed:
            self.cooldown = attackSpeed
        return super().cast(x, y)
