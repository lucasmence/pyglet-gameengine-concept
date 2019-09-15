import pyglet
from pyglet import font
from game import objects
from game import textures

class Hud(objects.Object):
    def __init__(self, mainBatch, unit):
        super().__init__()

        self.icons = []
        self.bars = []
        self.texts = []
        self.frame = None
        self.unit = unit
        self.tooltip = None

    def load(self, mainBatch):
        hudFrame = HudFrame(mainBatch, 0, 0)
        self.frame = hudFrame

        hudHealthBar = HudBar(mainBatch, 0, 120, 28)
        self.bars.append(hudHealthBar)

        hudEnergyBar = HudBar(mainBatch, 1, 120, 6)
        self.bars.append(hudEnergyBar)

        icon = 0
        title = 1
        description = 2

        resource = [None, None, None]
        if self.unit.attack != None:
            resource[icon] = self.unit.attack.icon
            resource[title] = self.unit.attack.title
            resource[description] = self.unit.attack.description

        hudAttackIcon = HudIcon(mainBatch, 'A', 109, 71, resource[icon], resource[title], resource[description])
        self.icons.append(hudAttackIcon)

        resource.clear()
        resource = [None, None, None]
        if self.unit.skillQ != None:
            resource[icon] = self.unit.skillQ.icon
            resource[title] = self.unit.skillQ.title
            resource[description] = self.unit.skillQ.description

        hudQIcon = HudIcon(mainBatch, 'Q', 154, 71, resource[icon], resource[title], resource[description])
        self.icons.append(hudQIcon)

        resource.clear()
        resource = [None, None, None]
        if self.unit.skillW != None:
            resource[icon] = self.unit.skillW.icon
            resource[title] = self.unit.skillW.title
            resource[description] = self.unit.skillW.description
        hudWIcon = HudIcon(mainBatch, 'W', 199, 71, resource[icon], resource[title], resource[description])
        self.icons.append(hudWIcon)

        resource.clear()
        resource = [None, None, None]
        if self.unit.skillE != None:
            resource[icon] = self.unit.skillE.icon
            resource[title] = self.unit.skillE.title
            resource[description] = self.unit.skillE.description
        hudEIcon = HudIcon(mainBatch, 'E', 244, 71, resource[icon], resource[title], resource[description])
        self.icons.append(hudEIcon)

        resource.clear()
        resource = [None, None, None]
        if self.unit.skillR != None:
            resource[icon] = self.unit.skillR.icon
            resource[title] = self.unit.skillR.title
            resource[description] = self.unit.skillR.description
        hudRIcon = HudIcon(mainBatch, 'R', 289, 71, resource[icon], resource[title], resource[description])
        self.icons.append(hudRIcon)

        resource.clear()
        hudUnitIcon = HudUnitIcon(mainBatch, 'unit', 28, 45, self.unit.icon)
        self.icons.append(hudUnitIcon)

        text = pyglet.text.Label('Armor:', x=20, y=10, batch=mainBatch, group=pyglet.graphics.OrderedGroup(12))
        text.font_name = 'Sprite Comic'
        text.font_size = 6

        text = pyglet.text.Label('Attack:', x=20, y=25, batch=mainBatch, group=pyglet.graphics.OrderedGroup(12))
        text.font_name = 'Sprite Comic'
        text.font_size = 6

        self.textArmor = pyglet.text.Label(str(self.unit.armor), x=70, y=10, batch=mainBatch, group=pyglet.graphics.OrderedGroup(12))
        self.textArmor.font_name = 'Sprite Comic'
        self.textArmor.font_size = 6

        self.textAttack = pyglet.text.Label('0', x=70, y=25, batch=mainBatch, group=pyglet.graphics.OrderedGroup(12))
        self.textAttack.font_name = 'Sprite Comic'
        self.textAttack.font_size = 6

        if self.unit.attack != None:
            self.textAttack.text = str(self.unit.attack.damage)

        font.add_file('game/fonts/sprite_comic.ttf')

    def update(self):
        if self.unit.attack != None:
            self.textAttack.text = str(self.unit.attack.damage)
        elif self.textAttack.text != '0':
            self.textAttack.text = '0'
        
        if self.unit.bonus.attack > 0:
            self.textAttack.text = str(int(self.textAttack.text) + self.unit.bonus.attack)
            self.textAttack.color = (50, 255, 50, 255)
        else:
            self.textAttack.color = (255, 255, 255, 255)
        
        
        self.textArmor.text = str(self.unit.armor)
        
        if self.unit.bonus.armor > 0:
            self.textArmor.text = str(int(self.textArmor.text) + self.unit.bonus.armor)
            self.textArmor.color = (50, 255, 50, 255)
        else:
            self.textArmor.color = (255, 255, 255, 255)
            

class HudFrame(objects.Object):
    def __init__(self, mainBatch, positionX, positionY):
        super().__init__()

        self.texture = pyglet.image.load('game/sprites/hud/unit-status-c.png')
        self.sprite = pyglet.sprite.Sprite(self.texture, x=positionX, y=positionY, batch=mainBatch, group=pyglet.graphics.OrderedGroup(10))   
        self.sprite.x = 20
       
        self.name = 'hud'
        self.type = 99

class HudUnitIcon():
    def __init__(self, mainBatch, key, positionX ,positionY, texture):

        self.scale = 0.70

        if (texture == None):
            texture = 'hud/icon-unit-unknown'

        self.key = key

        self.texture = pyglet.image.load('game/sprites/hud/'+texture+'.png')
        self.sprite = pyglet.sprite.Sprite(pyglet.image.load('game/sprites/hud/'+texture+'.png'), x=positionX, y=positionY, batch=mainBatch, group=pyglet.graphics.OrderedGroup(10))
        self.sprite.update(scale=self.scale)

    def showTooltip(self, positionX, positionY):
        pass

class HudIcon():
    def __init__(self, mainBatch, key, positionX ,positionY, texture, title, description):

        self.scale = 0.40

        if (texture == None):
            texture = 'icon-none'

        self.key = key

        self.texture = pyglet.image.load('game/sprites/hud/'+texture+'.png')
        self.sprite = pyglet.sprite.Sprite(pyglet.image.load('game/sprites/hud/'+texture+'.png'), x=positionX, y=positionY, batch=mainBatch, group=pyglet.graphics.OrderedGroup(10))
        self.sprite.update(scale=self.scale)

        self.textureLoad = pyglet.image.load('game/sprites/hud/frame-load-icon.png')
        self.spriteLoad = pyglet.sprite.Sprite(textures.texture_load('game/sprites/hud/frame-load-icon.png', 1, 1, 0, 100, 1, False), x=positionX, y=positionY, batch=mainBatch, group=pyglet.graphics.OrderedGroup(11))
        self.spriteLoad.opacity = 200
        self.spriteLoad.update(scale=0.80)

        self.text = pyglet.text.Label('', x=positionX + 7, y=positionY + 10, batch=mainBatch, group=pyglet.graphics.OrderedGroup(12))
        self.text.font_name = 'Sprite Comic'
        self.text.font_size = 8

        self.title = title
        self.description = description
        self.tooltip = None
        self.tooltipHud = None 
        if self.title != None and self.description != None:
            self.tooltipText = self.title + self.replicate((300 * 6) - (len(self.title) * 6)) + self.description
            self.tooltip = pyglet.text.Label(self.tooltipText, multiline=True, x=350, y=110, batch=self.sprite.batch, group=pyglet.graphics.OrderedGroup(13), width=300)
            self.tooltip.font_name = 'Sprite Comic'
            self.tooltip.font_size = 6
            self.tooltip.wrap = True
            self.tooltipHud = pyglet.sprite.Sprite(pyglet.image.load('game/sprites/hud/tooltip.png'), x=350, y=20, batch=mainBatch, group=pyglet.graphics.OrderedGroup(12))
            self.tooltipHud.opacity = 0

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

        if len(self.text.text) >= 5:
            self.text.font_size = 6
        else:
            self.text.font_size = 8

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
    
    def replicate(self, count):
        text = ''
        for index in range(count):
            text = text + ' '
        
        return text


    def showTooltip(self, positionX, positionY):
        if self.sprite != None and self.tooltip != None:
            if positionX < (self.sprite.x + self.sprite.width) and (self.sprite.x) < positionX \
            and positionY < (self.sprite.y + self.sprite.height) and (self.sprite.y) < positionY:
                if self.tooltip.color != (255, 255, 255, 255): 
                    self.tooltip.color = (255, 255, 255, 255)
                    self.tooltipHud.opacity = 255
            else:
                self.tooltip.color = (255, 255, 255, 0)    
                self.tooltipHud.opacity = 0

class HudBar():
    def __init__(self, mainBatch, barType, positionX ,positionY):

        if barType == 0:    
            self.texture = pyglet.image.load('game/sprites/hud/healthbar.png')
        else:
            self.texture = pyglet.image.load('game/sprites/hud/energybar.png')
        
        self.barType = barType
        self.sprite = pyglet.sprite.Sprite(textures.texture_load('game/sprites/hud/healthbar.png', 1, 1, 0, 100, 1, False), x=positionX, y=positionY, batch=mainBatch, group=pyglet.graphics.OrderedGroup(11))
        self.sprite.update(scale_y = 1, scale_x = 4)
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

        self.text = pyglet.text.Label('', x=positionX + self.sprite.width + 3, y=positionY + 3 , batch=mainBatch, group=pyglet.graphics.OrderedGroup(11))
        self.text.font_name = 'Sprite Comic'
        self.text.font_size = 6

        label = pyglet.text.Label('',  x=positionX - 20 , y=positionY + 3, batch=mainBatch, group=pyglet.graphics.OrderedGroup(11))
        label.font_name = 'Sprite Comic'
        label.font_size = 6

        if barType == 0:
            label.text = 'HP:'
        else:
            label.text = 'EP:'


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


