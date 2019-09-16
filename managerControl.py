import pyglet
from game import hud

class Manager():
    def __init__(self, batch):
        self.batch = batch

        self.units = []
        self.doodads = []
        self.missiles = []
        self.huds = []
        self.floatingTexts = []
        self.players = []
        self.stats = []
        self.buffs = []
        self.specialEffects = []
        self.texturePacks = []
        self.sounds = []
        self.tilesets = []
        self.terrain = []
    
    def update(self, dt, x, y):

        for unitObject in self.units:
            unitObject.update(dt)
            if unitObject.alive == False:
                self.units.remove(unitObject)
                del unitObject 

        for hudObject in self.huds:
            hudObject.update()
            showTooltip = False
            tooltipIcon = None
            tooltipData = None
            for icon in hudObject.icons:
                if showTooltip == False:
                    showTooltip = icon.showTooltip(x, y)
                    if showTooltip == True:
                        tooltipIcon = icon
                        if icon.key == 'A':
                            tooltipData = hudObject.unit.attack 
                        elif icon.key == 'Q':
                            tooltipData = hudObject.unit.skillQ
                        elif icon.key == 'W':
                            tooltipData = hudObject.unit.skillW
                        elif icon.key == 'E':
                            tooltipData = hudObject.unit.skillE   
                        elif icon.key == 'R':
                            tooltipData = hudObject.unit.skillR                   
                        
                if icon.key == 'A' and hudObject.unit.attack != None:
                    icon.update(hudObject.unit.attack.cooldownTime, hudObject.unit.attack.cooldown)
                if icon.key == 'Q' and hudObject.unit.skillQ != None:
                    icon.update(hudObject.unit.skillQ.cooldownTime, hudObject.unit.skillQ.cooldown)
                elif icon.key == 'W' and hudObject.unit.skillW != None:
                    icon.update(hudObject.unit.skillW.cooldownTime, hudObject.unit.skillW.cooldown)
                elif icon.key == 'E' and hudObject.unit.skillE != None:
                    icon.update(hudObject.unit.skillE.cooldownTime, hudObject.unit.skillE.cooldown)
                elif icon.key == 'R' and hudObject.unit.skillR != None:
                    icon.update(hudObject.unit.skillR.cooldownTime, hudObject.unit.skillR.cooldown)

            if showTooltip == True and tooltipData != None:
                if hudObject.tooltipIcon != tooltipIcon.key:
                    hudObject.tooltip.text = tooltipData.getTooltip()
                    hudObject.tooltipIcon = tooltipIcon.key       

                if hudObject.tooltipHud.opacity != 255: 
                    hudObject.tooltip.color = (255, 255, 255, 255)
                    hudObject.tooltipHud.opacity = 255

            elif hudObject.tooltipHud.color != 0 and showTooltip == False:
                hudObject.tooltip.color = (255, 255, 255, 0)    
                hudObject.tooltipHud.opacity = 0

            for bar in hudObject.bars:
                if bar.barType == 0:
                    bar.update(hudObject.unit.health, hudObject.unit.healthMax + hudObject.unit.bonus.healthMax)
                else:
                    bar.update(hudObject.unit.energy, hudObject.unit.energyMax + hudObject.unit.bonus.energyMax)

        for floatingTextObject in self.floatingTexts:
            if floatingTextObject.opacity < 100:
                floatingTextObject.update(dt)
            else:
                floatingTextObject.text.delete()
                self.floatingTexts.remove(floatingTextObject)
                del floatingTextObject
        
        for specialEffectObject in self.specialEffects:
            specialEffectObject.update(dt)
            if specialEffectObject.alive == False:
                specialEffectObject.sprite.delete()
                self.specialEffects.remove(specialEffectObject)
                del specialEffectObject 