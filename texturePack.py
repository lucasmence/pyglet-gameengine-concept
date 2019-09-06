import pyglet

class Texture():
    def __init__(self, x, y, height, width, time, sprite):
        self.sprite = sprite
        self.time = time
        self.x = x
        self.y = y
        self.height = height
        self.width = width

class TexturePack():

    def __init__(self, textureName):
        self.textureName = textureName
        self.textureFiles = None
        self.leftRightOnly = False

    def load(self):
        if self.textureName == 'anska':
            self.leftRightOnly = True
            self.textureFiles = {
                'stand' : [Texture(  6, 0, 50, 50, 0.50, 'game/sprites/characters/anska/anska-stand-down.png'),
                           Texture( 70, 0, 50, 50, 0.10, 'game/sprites/characters/anska/anska-stand-down.png'),
                           Texture(134, 0, 50, 50, 0.10, 'game/sprites/characters/anska/anska-stand-down.png'),
                           Texture(198, 0, 50, 50, 0.10, 'game/sprites/characters/anska/anska-stand-down.png'),
                           Texture(262, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-stand-down.png'),
                           Texture(326, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-stand-down.png'),
                           Texture(390, 0, 50, 50, 0.10, 'game/sprites/characters/anska/anska-stand-down.png')],

                'walk-left' : [Texture(  0, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-left.png'),
                               Texture( 65, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-left.png'),
                               Texture(130, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-left.png'),
                               Texture(190, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-left.png'),
                               Texture(252, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-left.png'),
                               Texture(315, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-left.png'),
                               Texture(380, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-left.png'),
                               Texture(445, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-left.png'),
                               Texture(510, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-left.png')],

                'walk-right' : [Texture(  0, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-right.png'),
                                Texture( 65, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-right.png'),
                                Texture(130, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-right.png'),
                                Texture(190, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-right.png'),
                                Texture(252, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-right.png'),
                                Texture(315, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-right.png'),
                                Texture(380, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-right.png'),
                                Texture(445, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-right.png'),
                                Texture(510, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-move-right.png')],

                'attack-right' : [Texture( 10, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-right.png'),
                                  Texture( 72, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-right.png'),
                                  Texture(135, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-right.png'),
                                  Texture(196, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-right.png'),
                                  Texture(265, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-right.png'),
                                  Texture(333, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-right.png'),
                                  Texture(393, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-right.png'),
                                  Texture(452, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-right.png')],

                'attack-left' : [Texture(  4, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-left.png'),
                                 Texture( 70, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-left.png'),
                                 Texture(135, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-left.png'),
                                 Texture(204, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-left.png'),
                                 Texture(260, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-left.png'),
                                 Texture(320, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-left.png'),
                                 Texture(388, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-left.png'),
                                 Texture(458, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-attack-left.png')],

                'death' : [Texture(  7, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-death.png'),
                           Texture( 72, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-death.png'),
                           Texture(135, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-death.png'),
                           Texture(200, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-death.png'),
                           Texture(265, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-death.png'),
                           Texture(328, 0, 50, 50, 0.05, 'game/sprites/characters/anska/anska-death.png')]
            }

        if self.textureName == 'skeleton-warrior':
            self.leftRightOnly = True
            self.textureFiles = {
                'stand' : [Texture(  7, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-stand-down.png'),
                           Texture( 71, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-stand-down.png'),
                           Texture(135, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-stand-down.png'),
                           Texture(199, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-stand-down.png'),
                           Texture(263, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-stand-down.png'),
                           Texture(327, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-stand-down.png'),
                           Texture(391, 0, 50, 50, 0.15, 'game/sprites/characters/skeleton-warrior/skeleton-stand-down.png')],

                'walk-left' : [Texture(  0, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-left.png'),
                               Texture( 71, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-left.png'),
                               Texture(135, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-left.png'),
                               Texture(199, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-left.png'),
                               Texture(263, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-left.png'),
                               Texture(327, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-left.png'),
                               Texture(391, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-left.png'),
                               Texture(455, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-left.png'),
                               Texture(519, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-left.png')],

                'walk-right' : [Texture(  0, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-right.png'),
                                Texture( 71, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-right.png'),
                                Texture(135, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-right.png'),
                                Texture(199, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-right.png'),
                                Texture(263, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-right.png'),
                                Texture(327, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-right.png'),
                                Texture(391, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-right.png'),
                                Texture(455, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-right.png'),
                                Texture(519, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-move-right.png')],

                'attack-right' : [Texture( 7, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-right.png'),
                                  Texture( 72, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-right.png'),
                                  Texture(136, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-right.png'),
                                  Texture(201, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-right.png'),
                                  Texture(267, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-right.png'),
                                  Texture(330, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-right.png')],

                'attack-left' : [Texture(  8, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-left.png'),
                                 Texture( 69, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-left.png'),
                                 Texture(134, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-left.png'),
                                 Texture(196, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-left.png'),
                                 Texture(260, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-left.png'),
                                 Texture(324, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-attack-left.png')],

                'death' : [Texture(  7, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-death.png'),
                           Texture( 72, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-death.png'),
                           Texture(135, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-death.png'),
                           Texture(200, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-death.png'),
                           Texture(265, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-death.png'),
                           Texture(328, 0, 50, 50, 0.05, 'game/sprites/characters/skeleton-warrior/skeleton-death.png')]
            }
