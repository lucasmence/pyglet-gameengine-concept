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
    
    def update(self, dt):

        for unitObject in self.units:
            unitObject.update(dt)
            if unitObject.alive == False:
                self.units.remove(unitObject)
                del unitObject 

        for hudObject in self.huds:
            for icon in hudObject.icons:
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