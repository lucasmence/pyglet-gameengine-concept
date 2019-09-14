import pyglet
from game import models
from game import textures

class Tileset():
    def __init__(self, textureName):
        self.textureName = textureName
        self.texture = None

        if self.textureName == 'castle-brick':
            self.texture = pyglet.image.load('game/sprites/block50x50.png')
        elif self.textureName == 'shuriken':
            self.texture = textures.texture_load('game/sprites/ninja-shuriken-25x.png', 1, 4, 25, 25, 0.02, True)    
        elif self.textureName == 'shield':
            self.texture = pyglet.image.load('game/sprites/characters/shield.png')
        elif self.textureName == 'shield-red':
            self.texture = pyglet.image.load('game/sprites/characters/shield-red.png')
        elif self.textureName == 'arrow':
            self.texture = pyglet.image.load('game/sprites/characters/arrow.png')
        elif self.textureName == 'slash':
            self.texture = pyglet.image.load('game/sprites/characters/slash.png')  
        elif self.textureName == 'dummy':
            self.texture = pyglet.image.load('game/sprites/characters/dummy.png')     

class TilesetEnchanter():
    def load(self, textureName, manager):
        result = None

        for tileset in manager.tilesets:
            if tileset.textureName == textureName:
                result = tileset
        
        if result == None:
            tileset = Tileset(textureName)
            manager.tilesets.append(tileset)
            result = tileset

        return result

class Texture():
    def __init__(self, aX, aY, aHeight, aWidth, aTime, aSpriteFile, aSprite):
        self.spriteFile = aSpriteFile
        self.time = aTime
        self.x = aX
        self.y = aY
        self.height = aHeight
        self.width = aWidth
        self.sprite = aSprite.image.from_image_sequence([pyglet.image.load(aSpriteFile).get_region(x=aX,y=aY,height=aHeight,width=aWidth)], 1, True)

class TexturePack():
    def __init__(self, textureName):
        self.textureName = textureName
        self.textureFiles = None
        self.leftRightOnly = False
      
    def load(self, sprite):
        if self.textureName == 'anska':
            self.leftRightOnly = True
            self.textureFiles = {
                'stand' : [Texture(  6, 0, 50, 50, 0.50, 'game/sprites/characters/anska/anska-stand-down.png', sprite),
                           Texture( 70, 0, 50, 50, 0.10, 'game/sprites/characters/anska/anska-stand-down.png', sprite),
                           Texture(134, 0, 50, 50, 0.10, 'game/sprites/characters/anska/anska-stand-down.png', sprite),
                           Texture(198, 0, 50, 50, 0.10, 'game/sprites/characters/anska/anska-stand-down.png', sprite),
                           Texture(262, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-stand-down.png', sprite),
                           Texture(326, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-stand-down.png', sprite),
                           Texture(390, 0, 50, 50, 0.10, 'game/sprites/characters/anska/anska-stand-down.png', sprite)],

                'walk-left' : [Texture(  0, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-left.png', sprite),
                               Texture( 65, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-left.png', sprite),
                               Texture(130, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-left.png', sprite),
                               Texture(190, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-left.png', sprite),
                               Texture(252, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-left.png', sprite),
                               Texture(315, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-left.png', sprite),
                               Texture(380, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-left.png', sprite),
                               Texture(445, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-left.png', sprite),
                               Texture(510, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-left.png', sprite)],

                'walk-right' : [Texture(  0, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-right.png', sprite),
                                Texture( 65, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-right.png', sprite),
                                Texture(130, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-right.png', sprite),
                                Texture(190, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-right.png', sprite),
                                Texture(252, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-right.png', sprite),
                                Texture(315, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-right.png', sprite),
                                Texture(380, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-right.png', sprite),
                                Texture(445, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-right.png', sprite),
                                Texture(510, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-right.png', sprite)],

                'attack-right' : [Texture( 10, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-right.png', sprite),
                                  Texture( 72, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-right.png', sprite),
                                  Texture(135, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-right.png', sprite),
                                  Texture(196, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-right.png', sprite),
                                  Texture(265, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-right.png', sprite),
                                  Texture(333, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-right.png', sprite),
                                  Texture(393, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-right.png', sprite),
                                  Texture(452, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-right.png', sprite)],

                'attack-left' : [Texture(  4, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-left.png', sprite),
                                 Texture( 70, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-left.png', sprite),
                                 Texture(135, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-left.png', sprite),
                                 Texture(204, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-left.png', sprite),
                                 Texture(260, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-left.png', sprite),
                                 Texture(320, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-left.png', sprite),
                                 Texture(388, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-left.png', sprite),
                                 Texture(458, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-left.png', sprite)],

                'death' : [Texture(  7, 0, 50, 50, 0.50, 'game/sprites/characters/anska/anska-death.png', sprite),
                           Texture( 72, 0, 50, 50, 0.50, 'game/sprites/characters/anska/anska-death.png', sprite),
                           Texture(135, 0, 50, 50, 0.50, 'game/sprites/characters/anska/anska-death.png', sprite),
                           Texture(200, 0, 50, 50, 0.50, 'game/sprites/characters/anska/anska-death.png', sprite),
                           Texture(265, 0, 50, 50, 0.50, 'game/sprites/characters/anska/anska-death.png', sprite),
                           Texture(328, 0, 50, 50, 2.00, 'game/sprites/characters/anska/anska-death.png', sprite)]
            }

        if self.textureName == 'skeleton-warrior':
            self.leftRightOnly = True
            self.textureFiles = {
                'stand' : [Texture(  7, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-stand.png', sprite),
                           Texture( 71, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-stand.png', sprite),
                           Texture(135, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-stand.png', sprite),
                           Texture(199, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-stand.png', sprite),
                           Texture(263, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-stand.png', sprite),
                           Texture(327, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-stand.png', sprite),
                           Texture(391, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-stand.png', sprite)],

                'walk-left' : [Texture(  0, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-left.png', sprite),
                               Texture( 71, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-left.png', sprite),
                               Texture(135, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-left.png', sprite),
                               Texture(199, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-left.png', sprite),
                               Texture(263, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-left.png', sprite),
                               Texture(327, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-left.png', sprite),
                               Texture(391, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-left.png', sprite),
                               Texture(455, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-left.png', sprite),
                               Texture(519, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-left.png', sprite)],

                'walk-right' : [Texture(  0, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-right.png', sprite),
                                Texture( 71, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-right.png', sprite),
                                Texture(135, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-right.png', sprite),
                                Texture(199, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-right.png', sprite),
                                Texture(263, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-right.png', sprite),
                                Texture(327, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-right.png', sprite),
                                Texture(391, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-right.png', sprite),
                                Texture(455, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-right.png', sprite),
                                Texture(519, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-right.png', sprite)],

                'attack-right' : [Texture(  7, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-right.png', sprite),
                                  Texture( 72, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-right.png', sprite),
                                  Texture(136, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-right.png', sprite),
                                  Texture(201, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-right.png', sprite),
                                  Texture(267, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-right.png', sprite),
                                  Texture(330, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-right.png', sprite)],

                'attack-left' : [Texture(  8, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-left.png', sprite),
                                 Texture( 69, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-left.png', sprite),
                                 Texture(134, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-left.png', sprite),
                                 Texture(196, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-left.png', sprite),
                                 Texture(260, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-left.png', sprite),
                                 Texture(324, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-left.png', sprite)],

                'death' : [Texture(  7, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-death.png', sprite),
                           Texture( 72, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-death.png', sprite),
                           Texture(135, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-death.png', sprite),
                           Texture(200, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-death.png', sprite),
                           Texture(265, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-death.png', sprite),
                           Texture(328, 0, 50, 50, 1.00, 'game/sprites/characters/skeleton-warrior/skeleton-death.png', sprite)]
            }
        
        if self.textureName == 'skeleton-archer':
            self.leftRightOnly = True
            self.textureFiles = {
                'stand' : [Texture(  7, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-archer/skeleton-stand.png', sprite),
                           Texture( 71, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-archer/skeleton-stand.png', sprite),
                           Texture(135, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-archer/skeleton-stand.png', sprite),
                           Texture(199, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-archer/skeleton-stand.png', sprite),
                           Texture(263, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-archer/skeleton-stand.png', sprite),
                           Texture(327, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-archer/skeleton-stand.png', sprite),
                           Texture(391, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-archer/skeleton-stand.png', sprite)],

                'walk-left' : [Texture(  0, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-archer/skeleton-move-left.png', sprite),
                               Texture( 71, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-archer/skeleton-move-left.png', sprite),
                               Texture(135, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-archer/skeleton-move-left.png', sprite),
                               Texture(199, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-archer/skeleton-move-left.png', sprite),
                               Texture(263, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-archer/skeleton-move-left.png', sprite),
                               Texture(327, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-archer/skeleton-move-left.png', sprite),
                               Texture(391, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-archer/skeleton-move-left.png', sprite),
                               Texture(455, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-archer/skeleton-move-left.png', sprite),
                               Texture(519, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-archer/skeleton-move-left.png', sprite)],

                'walk-right' : [Texture(  0, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-archer/skeleton-move-right.png', sprite),
                                Texture( 71, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-archer/skeleton-move-right.png', sprite),
                                Texture(135, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-archer/skeleton-move-right.png', sprite),
                                Texture(199, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-archer/skeleton-move-right.png', sprite),
                                Texture(263, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-archer/skeleton-move-right.png', sprite),
                                Texture(327, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-archer/skeleton-move-right.png', sprite),
                                Texture(391, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-archer/skeleton-move-right.png', sprite),
                                Texture(455, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-archer/skeleton-move-right.png', sprite),
                                Texture(519, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-archer/skeleton-move-right.png', sprite)],

                'attack-right' : [Texture(  7, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-right.png', sprite),
                                  Texture( 71, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-right.png', sprite),
                                  Texture(136, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-right.png', sprite),
                                  Texture(199, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-right.png', sprite),
                                  Texture(265, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-right.png', sprite),
                                  Texture(335, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-right.png', sprite),
                                  Texture(397, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-right.png', sprite),
                                  Texture(458, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-right.png', sprite),
                                  Texture(520, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-right.png', sprite),
                                  Texture(580, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-right.png', sprite),
                                  Texture(645, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-right.png', sprite),
                                  Texture(710, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-right.png', sprite),
                                  Texture(775, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-right.png', sprite)],

                'attack-left' : [Texture(  7, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-left.png', sprite),
                                 Texture( 71, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-left.png', sprite),
                                 Texture(136, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-left.png', sprite),
                                 Texture(199, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-left.png', sprite),
                                 Texture(260, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-left.png', sprite),
                                 Texture(320, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-left.png', sprite),
                                 Texture(385, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-left.png', sprite),
                                 Texture(452, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-left.png', sprite),
                                 Texture(520, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-left.png', sprite),
                                 Texture(580, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-left.png', sprite),
                                 Texture(645, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-left.png', sprite),
                                 Texture(710, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-left.png', sprite),
                                 Texture(770, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-archer/skeleton-attack-left.png', sprite)],

                'death' : [Texture(  7, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-death.png', sprite),
                           Texture( 72, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-death.png', sprite),
                           Texture(135, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-death.png', sprite),
                           Texture(200, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-death.png', sprite),
                           Texture(265, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-death.png', sprite),
                           Texture(328, 0, 50, 50, 1.00, 'game/sprites/characters/skeleton-warrior/skeleton-death.png', sprite)]
            }

        if self.textureName == 'skeleton-elite':
            self.leftRightOnly = True
            self.textureFiles = {
                'stand' : [Texture(  7, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-elite/skeleton-stand.png', sprite),
                           Texture( 71, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-elite/skeleton-stand.png', sprite),
                           Texture(135, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-elite/skeleton-stand.png', sprite),
                           Texture(199, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-elite/skeleton-stand.png', sprite),
                           Texture(263, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-elite/skeleton-stand.png', sprite),
                           Texture(327, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-elite/skeleton-stand.png', sprite),
                           Texture(391, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-elite/skeleton-stand.png', sprite)],

                'walk-left' : [Texture(  0, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-elite/skeleton-move-left.png', sprite),
                               Texture( 71, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-elite/skeleton-move-left.png', sprite),
                               Texture(135, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-elite/skeleton-move-left.png', sprite),
                               Texture(199, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-elite/skeleton-move-left.png', sprite),
                               Texture(263, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-elite/skeleton-move-left.png', sprite),
                               Texture(327, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-elite/skeleton-move-left.png', sprite),
                               Texture(391, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-elite/skeleton-move-left.png', sprite),
                               Texture(455, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-elite/skeleton-move-left.png', sprite),
                               Texture(519, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-elite/skeleton-move-left.png', sprite)],

                'walk-right' : [Texture(  0, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-elite/skeleton-move-right.png', sprite),
                                Texture( 71, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-elite/skeleton-move-right.png', sprite),
                                Texture(135, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-elite/skeleton-move-right.png', sprite),
                                Texture(199, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-elite/skeleton-move-right.png', sprite),
                                Texture(263, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-elite/skeleton-move-right.png', sprite),
                                Texture(327, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-elite/skeleton-move-right.png', sprite),
                                Texture(391, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-elite/skeleton-move-right.png', sprite),
                                Texture(455, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-elite/skeleton-move-right.png', sprite),
                                Texture(519, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-elite/skeleton-move-right.png', sprite)],

                'attack-right' : [Texture(  7, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-right.png', sprite),
                                  Texture( 71, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-right.png', sprite),
                                  Texture(136, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-right.png', sprite),
                                  Texture(199, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-right.png', sprite),
                                  Texture(265, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-right.png', sprite),
                                  Texture(335, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-right.png', sprite),
                                  Texture(397, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-right.png', sprite),
                                  Texture(458, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-right.png', sprite),
                                  Texture(520, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-right.png', sprite),
                                  Texture(580, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-right.png', sprite),
                                  Texture(645, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-right.png', sprite),
                                  Texture(710, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-right.png', sprite),
                                  Texture(775, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-right.png', sprite)],

                'attack-left' : [Texture(  7, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-left.png', sprite),
                                 Texture( 71, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-left.png', sprite),
                                 Texture(136, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-left.png', sprite),
                                 Texture(199, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-left.png', sprite),
                                 Texture(260, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-left.png', sprite),
                                 Texture(320, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-left.png', sprite),
                                 Texture(385, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-left.png', sprite),
                                 Texture(452, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-left.png', sprite),
                                 Texture(520, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-left.png', sprite),
                                 Texture(580, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-left.png', sprite),
                                 Texture(645, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-left.png', sprite),
                                 Texture(710, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-left.png', sprite),
                                 Texture(770, 0, 55, 50, 0.01, 'game/sprites/characters/skeleton-elite/skeleton-attack-left.png', sprite)],

                'death' : [Texture(  7, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-elite/skeleton-death.png', sprite),
                           Texture( 72, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-elite/skeleton-death.png', sprite),
                           Texture(135, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-elite/skeleton-death.png', sprite),
                           Texture(200, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-elite/skeleton-death.png', sprite),
                           Texture(265, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-elite/skeleton-death.png', sprite),
                           Texture(328, 0, 50, 50, 1.00, 'game/sprites/characters/skeleton-elite/skeleton-death.png', sprite)]
            }

        if self.textureName == 'dummy':
            self.leftRightOnly = True
            self.textureFiles = {
                'stand' : [Texture(  0, 0, 50, 50, 1.00, 'game/sprites/characters/dummy.png', sprite)]
            }
        
        if self.textureName == 'warrior':
            self.leftRightOnly = True
            self.textureFiles = {
                'stand' : [Texture(  7, 0, 50, 50, 0.30, 'game/sprites/characters/warrior/warrior-stand.png', sprite),
                           Texture(  7, 0, 50, 50, 0.30, 'game/sprites/characters/warrior/warrior-stand.png', sprite),
                           Texture( 71, 0, 50, 50, 0.30, 'game/sprites/characters/warrior/warrior-stand.png', sprite),
                           Texture(135, 0, 50, 50, 0.30, 'game/sprites/characters/warrior/warrior-stand.png', sprite),
                           Texture( 71, 0, 50, 50, 0.30, 'game/sprites/characters/warrior/warrior-stand.png', sprite),
                           Texture(  7, 0, 50, 50, 0.30, 'game/sprites/characters/warrior/warrior-stand.png', sprite)],

                'walk-left' : [Texture(  0, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-move-left.png', sprite),
                               Texture( 71, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-move-left.png', sprite),
                               Texture(135, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-move-left.png', sprite),
                               Texture(199, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-move-left.png', sprite),
                               Texture(263, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-move-left.png', sprite),
                               Texture(327, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-move-left.png', sprite),
                               Texture(391, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-move-left.png', sprite),
                               Texture(455, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-move-left.png', sprite),
                               Texture(519, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-move-left.png', sprite)],

                'walk-right' : [Texture(  0, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-move-right.png', sprite),
                                Texture( 71, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-move-right.png', sprite),
                                Texture(135, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-move-right.png', sprite),
                                Texture(199, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-move-right.png', sprite),
                                Texture(263, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-move-right.png', sprite),
                                Texture(327, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-move-right.png', sprite),
                                Texture(391, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-move-right.png', sprite),
                                Texture(455, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-move-right.png', sprite),
                                Texture(519, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-move-right.png', sprite)],

                'attack-right' : [Texture(  7, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-attack-right.png', sprite),
                                  Texture( 72, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-attack-right.png', sprite),
                                  Texture(136, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-attack-right.png', sprite),
                                  Texture(201, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-attack-right.png', sprite),
                                  Texture(267, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-attack-right.png', sprite),
                                  Texture(330, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-attack-right.png', sprite)],

                'attack-left' : [Texture(  8, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-attack-left.png', sprite),
                                 Texture( 69, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-attack-left.png', sprite),
                                 Texture(134, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-attack-left.png', sprite),
                                 Texture(196, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-attack-left.png', sprite),
                                 Texture(260, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-attack-left.png', sprite),
                                 Texture(324, 0, 50, 50, 0.05, 'game/sprites/characters/warrior/warrior-attack-left.png', sprite)],

                'death' : [Texture(  7, 0, 50, 50, 0.15, 'game/sprites/characters/warrior/warrior-death.png', sprite),
                           Texture( 72, 0, 50, 50, 0.15, 'game/sprites/characters/warrior/warrior-death.png', sprite),
                           Texture(135, 0, 50, 50, 0.15, 'game/sprites/characters/warrior/warrior-death.png', sprite),
                           Texture(200, 0, 50, 50, 0.15, 'game/sprites/characters/warrior/warrior-death.png', sprite),
                           Texture(265, 0, 50, 50, 0.15, 'game/sprites/characters/warrior/warrior-death.png', sprite),
                           Texture(328, 0, 50, 50, 1.00, 'game/sprites/characters/warrior/warrior-death.png', sprite)]
            }

class TextureEnchanter():
    def load(self, textureName, sprite, manager):
        result = None

        for texture in manager.texturePacks:
            if texture.textureName == textureName:
                result = texture
        
        if result == None:
            texture = TexturePack(textureName)
            texture.load(sprite)
            manager.texturePacks.append(texture)
            result = texture

        return result