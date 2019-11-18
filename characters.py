import pyglet
from game import units
from game import abilities
from game import attackTypes
from game import collision

class BaseUnit(units.Unit):
    def __init__(self, mainBatch, positionX, positionY, owner, manager):    
        super().__init__(mainBatch, positionX, positionY, owner, manager)

        self.sprite.update(scale=1.00)
        self.name = 'base-unit'
        self.attackSpeed = 0.5
        self.healthMax = 100
        self.healthRegeneration = 0.2
        self.energyMax = 100 
        self.armor = 0
        self.movementSpeed = 150
        self.health = self.healthMax + self.bonus.healthMax 

######################################################################################################################################

class Hero(BaseUnit):
    def __init__(self, mainBatch, positionX, positionY, owner, manager):    
        super().__init__(mainBatch, positionX, positionY, owner, manager)
        
        self.model.load('warrior', '', manager)

        self.sprite.update(scale=1.00)
        self.name = 'hero'
        self.attackSpeed = 0.3
        self.healthMax = 100
        self.healthRegeneration = 0.2
        self.energyMax = 20
        self.energy = self.energyMax
        self.armor = 10
        self.movementSpeed = 120
        self.icon = 'icon-warrior'

        self.skillQ = abilities.ShurikenCone(self, self.manager)
        self.skillW = abilities.ShieldBlock(self, self.manager)
        self.skillE = abilities.FlameSword(self, self.manager)
        self.skillR = abilities.SteelStorm(self, self.manager)

        self.attack = attackTypes.Slash(self, self.manager) 
        self.attack.damage = 2

        self.health = self.healthMax + self.bonus.healthMax

        self.sprite.image = self.model.texturePack.textureFiles['stand'][0].sprite

class HeroRanger(BaseUnit):
    def __init__(self, mainBatch, positionX, positionY, owner, manager):    
        super().__init__(mainBatch, positionX, positionY, owner, manager)
        
        self.model.load('ranger', '', manager)

        self.sprite.update(scale=1.00)
        self.name = 'hero-ranger'
        self.attackSpeed = 0.5
        self.healthMax = 40
        self.healthRegeneration = 0.1
        self.energyMax = 30
        self.energy = self.energyMax
        self.energyRegeneration = 0.7
        self.armor = 5
        self.movementSpeed = 180
        self.icon = 'icon-ranger'

        self.skillQ = abilities.ArrowVolley(self, self.manager)
        self.skillW = abilities.SinisterAura(self, self.manager)
        self.skillE = abilities.SoulArrows(self, self.manager)
        self.skillR = abilities.Shockwave(self, self.manager)

        self.attack = attackTypes.ArrowRanger(self, self.manager) 

        self.health = self.healthMax + self.bonus.healthMax

        self.sprite.image = self.model.texturePack.textureFiles['stand'][0].sprite

class SkeletonWarrior(BaseUnit):  
    def __init__(self, mainBatch, positionX, positionY, owner, manager):    
        super().__init__(mainBatch, positionX, positionY, owner, manager)

        self.model.load('skeleton-warrior', '', manager)

        self.name = 'skeleton-warrior'
        self.attackSpeed = 1
        self.healthMax = 10
        self.energyMax = 10 
        self.energyRegeneration = 0.2
        self.healthRegeneration = 0.00
        self.armor = 0
        self.movementSpeed = 20
        self.minimumRange = 50

        self.skillQ = None
        self.attack = attackTypes.Slash(self, self.manager) 

        self.sprite.image = self.model.texturePack.textureFiles['stand'][0].sprite
    
    def update(self, dt):
        self.moving = True
        distance = collision.distance(self.diferenceX, self.diferenceY)
        super().update(dt)

        if  (self.diferenceX != 0) and (self.diferenceY != 0):
            if (collision.distance(self.diferenceX, self.diferenceY) <= 100):
                self.cast(self.A, self.moveX, self.moveY)  

class SkeletonArcher(BaseUnit):  
    def __init__(self, mainBatch, positionX, positionY, owner, manager):    
        super().__init__(mainBatch, positionX, positionY, owner, manager)

        self.model.load('skeleton-archer', '', manager)

        self.name = 'skeleton-archer'
        self.attackSpeed = 2.25
        self.healthMax = 10
        self.energyMax = 10 
        self.energyRegeneration = 0.2
        self.healthRegeneration = 0.00
        self.armor = 0
        self.movementSpeed = 20
        self.minimumRange = 400

        self.skillQ = None
        self.attack = attackTypes.Arrow(self, self.manager) 

        self.sprite.image = self.model.texturePack.textureFiles['stand'][0].sprite
    
    def update(self, dt):
        self.moving = True
        distance = collision.distance(self.diferenceX, self.diferenceY)
        super().update(dt)

        if  (self.diferenceX != 0) and (self.diferenceY != 0):
            if (collision.distance(self.diferenceX, self.diferenceY) <= 500):
                self.cast(self.A, self.moveX, self.moveY)  

class SkeletonElite(BaseUnit):  
    def __init__(self, mainBatch, positionX, positionY, owner, manager):    
        super().__init__(mainBatch, positionX, positionY, owner, manager)

        self.model.load('skeleton-elite', '', manager)

        self.name = 'skeleton-elite'
        self.attackSpeed = 2.50
        self.healthMax = 20
        self.energyMax = 20 
        self.energyRegeneration = 0.75
        self.healthRegeneration = 0.10
        self.armor = 20
        self.movementSpeed = 15
        self.minimumRange = 400

        self.skillQ = abilities.BlackShield(self, self.manager)
        self.attack = attackTypes.ArrowCone(self, self.manager) 

        self.sprite.image = self.model.texturePack.textureFiles['stand'][0].sprite
    
    def update(self, dt):
        self.moving = True
        distance = collision.distance(self.diferenceX, self.diferenceY)
        super().update(dt)

        if  (self.diferenceX != 0) and (self.diferenceY != 0):
            if (collision.distance(self.diferenceX, self.diferenceY) <= 400):
                self.cast(self.A, self.moveX, self.moveY)  

            if (self.skillQ.cooldownTime >= self.skillQ.cooldown):
                self.cast(self.Q, self.moveX, self.moveY)  

class Boss(BaseUnit):
    def __init__(self, mainBatch, positionX, positionY, owner, manager):    
        super().__init__(mainBatch, positionX, positionY, owner, manager)
        
        self.model.load('mini-boss', '', manager)

        self.sprite.update(scale=1.00)
        self.name = 'boss'
        self.attackSpeed = 0.3
        self.healthMax = 50
        self.healthRegeneration = 0.2
        self.energyMax = 20
        self.energyRegeneration = 5.00
        self.armor = 10
        self.movementSpeed = 100
        self.icon = 'icon-warrior'

        self.skillQ = abilities.ShurikenCone(self, self.manager)
        self.skillW = abilities.ShieldBlock(self, self.manager)
        self.skillE = abilities.Shockwave(self, self.manager)
        self.skillR = abilities.SteelStorm(self, self.manager)
        self.skillQ.cooldown = 3.00
        self.skillR.cooldownStep = [5.00, 3.00]

        self.attack = attackTypes.Slash(self, self.manager) 
        self.attack.damage = 2

        self.health = self.healthMax + self.bonus.healthMax

        self.sprite.image = self.model.texturePack.textureFiles['stand'][0].sprite

    def update(self, dt):
        self.moving = True
        distance = collision.distance(self.diferenceX, self.diferenceY)
        super().update(dt)

        if  (self.diferenceX != 0) and (self.diferenceY != 0):
            if (collision.distance(self.diferenceX, self.diferenceY) <= 100):
                self.cast(self.A, self.moveX, self.moveY)  
            
            if (self.skillQ.cooldownTime >= self.skillQ.cooldown) and (collision.distance(self.diferenceX, self.diferenceY) <= 200):
                self.cast(self.Q, self.moveX, self.moveY)  

            if (self.skillW.cooldownTime >= self.skillW.cooldown) and (collision.distance(self.diferenceX, self.diferenceY) <= 100):
                self.cast(self.W, self.moveX, self.moveY)  
            
            if (self.skillR.cooldownTime >= self.skillR.cooldown):
                self.cast(self.R, self.moveX, self.moveY)  
            
            if (self.skillE.cooldownTime >= self.skillE.cooldown):
                self.cast(self.E, self.moveX, self.moveY)  