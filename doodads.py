import pyglet

from game import objects


class Doodad(objects.Object):
    def __init__(self, mainBatch, positionX, positionY):
        super().__init__()

        self.texture = pyglet.image.load('game/sprites/block50x50.png')
        self.sprite = pyglet.sprite.Sprite(self.texture, x=positionX, y=positionY, batch=mainBatch, group=pyglet.graphics.OrderedGroup(0))       
       
        self.name = 'doodad'
        self.type = 2

        self.health = 10
        self.invulnerable = True
        
        self.angle = 0

class CastleBlock(Doodad):
    def __init__(self, mainBatch, positionX, positionY):
        super().__init__(mainBatch, positionX, positionY)

        self.texture = pyglet.image.load('game/sprites/block50x50.png')
        self.sprite.image = self.texture
        self.sprite.update(scale = 0.50)
       
        self.name = 'castle_block'
