import pyglet
from pyglet import font
from game import objects
from game import textures

class Hud(objects.Object):
    def __init__(self, mainBatch, player):
        super().__init__()

        self.icons = []
        self.bars = []
        self.texts = []
        self.frame = None
        self.player = player

    def load(self, mainBatch):
        hudFrame = HudFrame(mainBatch, 0, 0)
        self.frame = hudFrame

        hudHealthBar = HudBar(mainBatch, 0, 50, 40)
        self.bars.append(hudHealthBar)

        hudEnergyBar = HudBar(mainBatch, 1, 50, 10)
        self.bars.append(hudEnergyBar)

        hudQIcon = HudIcon(mainBatch, 'Q', 500, 40, 'icon-shuriken.png')
        self.icons.append(hudQIcon)

        hudWIcon = HudIcon(mainBatch, 'W', 560, 40, 'icon-shield-block.png')
        self.icons.append(hudWIcon)

        hudEIcon = HudIcon(mainBatch, 'E', 620, 40, None)
        self.icons.append(hudEIcon)

        hudRIcon = HudIcon(mainBatch, 'R', 680, 40, 'icon-steel-storm.png')
        self.icons.append(hudRIcon)

        font.add_file('game/fonts/sprite_comic.ttf')
        
        text = pyglet.text.Label("Q", x=520, y=10, batch=mainBatch)
        text.font_name = 'Sprite Comic'
        text.font_size = 8
        self.texts.append(text)

        text = pyglet.text.Label("W", x=580, y=10, batch=mainBatch)
        text.font_name = 'Sprite Comic'
        text.font_size = 8
        self.texts.append(text)

        text = pyglet.text.Label("E", x=640, y=10, batch=mainBatch)
        text.font_name = 'Sprite Comic'
        text.font_size = 8
        self.texts.append(text)

        text = pyglet.text.Label("R", x=700, y=10, batch=mainBatch)
        text.font_name = 'Sprite Comic'
        text.font_size = 8
        self.texts.append(text)

        text = pyglet.text.Label("HP: ", x=20 , y=50, batch=mainBatch)
        text.font_name = 'Sprite Comic'
        text.font_size = 8
        self.texts.append(text)

        text = pyglet.text.Label("EP: ", x=20 , y=15, batch=mainBatch)
        text.font_name = 'Sprite Comic'
        text.font_size = 8
        self.texts.append(text)

class HudFrame(objects.Object):
    def __init__(self, mainBatch, positionX, positionY):
        super().__init__()

        self.texture = pyglet.image.load('game/sprites/frame-main.png')
        self.sprite = pyglet.sprite.Sprite(self.texture, x=positionX, y=positionY, batch=mainBatch)   
       
        self.name = 'hud'
        self.type = 99

class HudIcon():
    def __init__(self, mainBatch, key, positionX ,positionY, texture):

        if (texture == None):
            texture = 'icon-none.png'

        self.key = key

        self.texture = pyglet.image.load('game/sprites/'+texture)
        self.sprite = pyglet.sprite.Sprite(pyglet.image.load('game/sprites/'+texture), x=positionX, y=positionY, batch=mainBatch, group=pyglet.graphics.OrderedGroup(0))
        self.sprite.update(scale = 0.50)

        self.textureLoad = pyglet.image.load('game/sprites/frame-load-icon.png')
        self.spriteLoad = pyglet.sprite.Sprite(textures.texture_load('game/sprites/frame-load-icon.png', 1, 1, 0, 100, 1, False), x=positionX, y=positionY, batch=mainBatch, group=pyglet.graphics.OrderedGroup(1))
        self.spriteLoad.opacity = 200
        self.spriteLoad.update(scale = 1.00)

        self.text = pyglet.text.Label('', x=positionX + 15, y=positionY + 20, batch=mainBatch, group=pyglet.graphics.OrderedGroup(2))
        self.text.font_name = 'Sprite Comic'
        self.text.font_size = 8

        self.animationLoad100 = self.spriteLoad.image.from_image_sequence([self.textureLoad.get_region(x=450,y=0,height=50,width=50)], 0.01, True)
        self.animationLoad090 = self.spriteLoad.image.from_image_sequence([self.textureLoad.get_region(x=400,y=0,height=50,width=50)], 0.01, True)
        self.animationLoad080 = self.spriteLoad.image.from_image_sequence([self.textureLoad.get_region(x=350,y=0,height=50,width=50)], 0.01, True)
        self.animationLoad070 = self.spriteLoad.image.from_image_sequence([self.textureLoad.get_region(x=300,y=0,height=50,width=50)], 0.01, True)
        self.animationLoad060 = self.spriteLoad.image.from_image_sequence([self.textureLoad.get_region(x=250,y=0,height=50,width=50)], 0.01, True)
        self.animationLoad050 = self.spriteLoad.image.from_image_sequence([self.textureLoad.get_region(x=200,y=0,height=50,width=50)], 0.01, True)
        self.animationLoad040 = self.spriteLoad.image.from_image_sequence([self.textureLoad.get_region(x=150,y=0,height=50,width=50)], 0.01, True)
        self.animationLoad030 = self.spriteLoad.image.from_image_sequence([self.textureLoad.get_region(x=100,y=0,height=50,width=50)], 0.01, True)
        self.animationLoad020 = self.spriteLoad.image.from_image_sequence([self.textureLoad.get_region(x=50,y=0,height=50,width=50)], 0.01, True)
        self.animationLoad010 = self.spriteLoad.image.from_image_sequence([self.textureLoad.get_region(x=0,y=0,height=50,width=50)], 0.01, True)
        self.animationLoad000 = self.spriteLoad.image.from_image_sequence([self.textureLoad.get_region(x=500,y=0,height=50,width=50)], 0.01, True)   
        self.spriteLoad.image = self.animationLoad000
        self.type = 98

    def update(self, value, valueMax):
        percentage = value / valueMax
        self.text.text = "{0:.1f}".format(valueMax - value)
        if percentage >= 1.00:
            self.spriteLoad.image = self.animationLoad000 
            self.text.text = ''
        elif percentage > 0.90:
            self.spriteLoad.image = self.animationLoad010
        elif percentage > 0.80:
            self.spriteLoad.image = self.animationLoad020
        elif percentage > 0.70:
            self.spriteLoad.image = self.animationLoad030  
        elif percentage > 0.60:
            self.spriteLoad.image = self.animationLoad040 
        elif percentage > 0.50:
            self.spriteLoad.image = self.animationLoad050 
        elif percentage > 0.40:
            self.spriteLoad.image = self.animationLoad060
        elif percentage > 0.30:
            self.spriteLoad.image = self.animationLoad070
        elif percentage > 0.20:
            self.spriteLoad.image = self.animationLoad080  
        elif percentage > 0.10:
            self.spriteLoad.image = self.animationLoad090 
        elif percentage > 0.00:
            self.spriteLoad.image = self.animationLoad100 


class HudBar():
    def __init__(self, mainBatch, barType, positionX ,positionY):

        if barType == 0:    
            self.texture = pyglet.image.load('game/sprites/healthbar.png')
        else:
            self.texture = pyglet.image.load('game/sprites/energybar.png')
        
        self.barType = barType
        self.sprite = pyglet.sprite.Sprite(textures.texture_load('game/sprites/healthbar.png', 1, 1, 0, 100, 1, False), x=positionX, y=positionY, batch=mainBatch)
        self.sprite.update(scale_y = 2, scale_x = 8)
        self.animation100 = self.sprite.image.from_image_sequence([self.texture.get_region(x=450,y=0,height=15,width=50)], 1, True)
        self.animation090 = self.sprite.image.from_image_sequence([self.texture.get_region(x=400,y=0,height=15,width=50)], 1, True)
        self.animation080 = self.sprite.image.from_image_sequence([self.texture.get_region(x=350,y=0,height=15,width=50)], 1, True)
        self.animation070 = self.sprite.image.from_image_sequence([self.texture.get_region(x=300,y=0,height=15,width=50)], 1, True)
        self.animation060 = self.sprite.image.from_image_sequence([self.texture.get_region(x=250,y=0,height=15,width=50)], 1, True)
        self.animation050 = self.sprite.image.from_image_sequence([self.texture.get_region(x=200,y=0,height=15,width=50)], 1, True)
        self.animation040 = self.sprite.image.from_image_sequence([self.texture.get_region(x=150,y=0,height=15,width=50)], 1, True)
        self.animation030 = self.sprite.image.from_image_sequence([self.texture.get_region(x=100,y=0,height=15,width=50)], 1, True)
        self.animation020 = self.sprite.image.from_image_sequence([self.texture.get_region(x=50,y=0,height=15,width=50)], 1, True)
        self.animation010 = self.sprite.image.from_image_sequence([self.texture.get_region(x=0,y=0,height=15,width=50)], 1, True)
        self.animation000 = self.sprite.image.from_image_sequence([self.texture.get_region(x=500,y=0,height=15,width=50)], 1, True)    

        self.sprite.image = self.animation100
        self.type = 99

        self.text = pyglet.text.Label('', x=positionX + self.sprite.width + 10, y=positionY + 10 , batch=mainBatch, group=pyglet.graphics.OrderedGroup(2))
        self.text.font_name = 'Sprite Comic'
        self.text.font_size = 8

    def update(self, value, valueMax):
        self.text.text = str(round(value))

        percentage = value / valueMax
        if percentage > 0.95:
            self.sprite.image = self.animation100 
        elif percentage > 0.85:
            self.sprite.image = self.animation090
        elif percentage > 0.75:
            self.sprite.image = self.animation080
        elif percentage > 0.65:
            self.sprite.image = self.animation070  
        elif percentage > 0.55:
            self.sprite.image = self.animation060 
        elif percentage > 0.45:
            self.sprite.image = self.animation050 
        elif percentage > 0.35:
            self.sprite.image = self.animation040
        elif percentage > 0.25:
            self.sprite.image = self.animation030
        elif percentage > 0.15:
            self.sprite.image = self.animation020  
        elif percentage > 0.10:
            self.sprite.image = self.animation010 
        elif percentage > 0.00:
            self.sprite.image = self.animation000 


