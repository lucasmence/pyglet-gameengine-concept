import pyglet
import random

from game import floatingText

class Damage():
    def __init__(self, damage, lifesteal, criticalChance, caster, target, manager):

        armor = (1 - ((target.armor + target.bonus.armor) / 100))
        if armor < 0:
            armor = 0
        if damage < 0:
            damage = 0
        damageValue = damage * armor

        criticalValue = random.randint(1,100)
        critical = False
        criticalHeal = False
        if criticalValue <= criticalChance + caster.bonus.critical:
            critical = True
            damageValue = damageValue * 2

        target.health -= damageValue
        if lifesteal < 0:
            lifesteal = damageValue * (lifesteal * -1)
            criticalHeal = critical

        useCurrentText = False
        for objectText in manager.floatingTexts:
            if objectText.unit == target and objectText.valueType == 0 and objectText.opacity < 50 and objectText.critical == False:
                useCurrentText = True
                objectText.value = objectText.value + damageValue
                objectText.opacity = 0
                objectText.text.y = objectText.unit.sprite.y
        if useCurrentText == False:
            if damageValue > 0.5:
                textDamage = floatingText.FloatingText(caster.batch, target, damageValue, 0, critical)
                manager.floatingTexts.append(textDamage)
        
        if lifesteal > 0:
            heal = Heal(lifesteal, criticalHeal, caster, caster, manager)
            del heal

class Heal():
    def __init__(self, heal, critical, caster, target, manager):

        target.health += heal

        if target.health > target.healthMax + target.bonus.healthMax:
            target.health = target.healthMax + target.bonus.healthMax

        useCurrentText = False
        for objectText in manager.floatingTexts:
            if objectText.unit == target and objectText.valueType == 1 and objectText.opacity < 50 and objectText.critical == False:
                useCurrentText = True
                objectText.value = objectText.value + heal
                objectText.opacity = 0
                objectText.text.y = objectText.unit.sprite.y

        if useCurrentText == False:
            textDamage = floatingText.FloatingText(caster.batch, target, heal, 1, critical)
            manager.floatingTexts.append(textDamage)