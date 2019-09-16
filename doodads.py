import pyglet

from game import objects
from game import texturePacks


class Doodad(objects.Object):
    def __init__(self, mainBatch, positionX, positionY, manager):
        super().__init__()

        tilesetEnchanter = texturePacks.TilesetEnchanter()
        self.tileset = tilesetEnchanter.load('dummy', manager)
        del tilesetEnchanter

        self.sprite = pyglet.sprite.Sprite(self.tileset.texture, x=positionX, y=positionY, batch=mainBatch, group=pyglet.graphics.OrderedGroup(0))       
       
        self.name = 'doodad'
        self.type = 2

        self.health = 10
        self.invulnerable = True
        
        self.angle = 0

class CastleBlock(Doodad):
    def __init__(self, mainBatch, positionX, positionY, manager):
        super().__init__(mainBatch, positionX, positionY, manager)
        
        tilesetEnchanter = texturePacks.TilesetEnchanter()
        self.tileset = tilesetEnchanter.load('castle-brick', manager)
        del tilesetEnchanter

        self.sprite.image = self.tileset.texture
        self.sprite.update(scale = 0.50)
       
        self.name = 'castle-brick'

class Terrain(Doodad):
    def __init__(self, terrain, positionX, positionY, mainBatch, manager):
        super().__init__(mainBatch, positionX, positionY, manager)
        
        tilesetEnchanter = texturePacks.TilesetEnchanter()
        self.tileset = tilesetEnchanter.load(terrain, manager)
        del tilesetEnchanter

        self.sprite.image = self.tileset.texture
               
        self.name = 'terrain'

