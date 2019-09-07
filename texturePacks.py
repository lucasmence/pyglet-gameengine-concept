import pyglet
from game import models

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

                'death' : [Texture(  7, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-death.png', sprite),
                           Texture( 72, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-death.png', sprite),
                           Texture(135, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-death.png', sprite),
                           Texture(200, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-death.png', sprite),
                           Texture(265, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-death.png', sprite),
                           Texture(328, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-death.png', sprite)]
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