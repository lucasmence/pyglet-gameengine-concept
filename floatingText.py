import pyglet
from pyglet import font
from game import objects

import random

class FloatingText(objects.Object):
    def __init__(self, mainBatch, unit, value, valueType):
        super().__init__()

        font.add_file('game/fonts/sprite_comic.ttf')
        if value < 1:
            value = 1
        
        self.valueType = valueType
        self.unit = unit
        self.text = pyglet.text.Label(str(int(value)), x=self.unit.sprite.x + random.randint(0,self.unit.sprite.width), y=self.unit.sprite.y + random.randint(0,self.unit.sprite.height), batch=mainBatch)
        self.text.font_name = 'Sprite Comic'
        self.text.font_size = 8
        self.opacity = 0
        self.red = 255
        self.green = 255
        self.blue = 255

        if valueType == 0:
            self.red = 255
            self.green = 100
            self.blue = 100 
        elif valueType == 1:
            self.red = 100
            self.green = 255
            self.blue = 100    

        self.type = 30

    def update(self, dt):
        if self.opacity < 100:
            self.opacity += 70 * dt
            self.text.color = (self.red, self.green, self.blue, int(255 - (self.opacity * 2.55)))
            self.text.y = self.text.y + 100 * dt 