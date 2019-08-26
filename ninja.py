import pyglet
from pyglet.window import key
from pyglet.window import FPSDisplay
from pyglet.window import mouse
from pyglet import font
from game import textures
from game import units
from game import doodads
from game import hud

def circle(x, y, radius, dt):
    global testBlock
    import math
    global execute, i, iterations, c, s, dx, dy
    if not execute:
        execute = True
        iterations = int(2*radius*math.pi) * 0.2
        s = math.sin(2*math.pi / iterations)
        c = math.cos(2*math.pi / iterations) 
        i = 0
        dx, dy = radius, 0

    #for i in range(iterations+1): 
    if i < iterations+1:   
        testBlock.sprite.x = (x + dx)
        testBlock.sprite.y = (y + dy)
        dx, dy = (dx*c - dy*s), (dy*c + dx*s)
        i += 1
    else:
        execute = False
        

def display_window_preload():
    global window
    window = pyglet.window.Window(width=1200, height=800, caption="goeninjas", resizable=False)
    window.set_location(400, 100)

    global main_batch
    main_batch = pyglet.graphics.Batch()

def texture_load_all():
    global texture_block_50x50
    texture_block_50x50 = pyglet.image.load('game/sprites/block50x50.png')

def display_fps_show():
    global window
    global display_fps
    display_fps = FPSDisplay(window)
    display_fps.label.font_size = 10
    display_fps.label.y = 10
    display_fps.label.x = 1155
    display_fps.label.color = (0,255,0,255)

def display_hud():
    font.add_file('game/fonts/sprite_comic.ttf')

    global text_hp_value, text_ep_value
    text_hp = pyglet.text.Label("HP: ", x=20 , y=50, batch=main_batch)
    text_hp.font_name = 'Sprite Comic'
    text_hp.font_size = 8

    text_hp_value = pyglet.text.Label("0", x=460 , y=50, batch=main_batch)
    text_hp_value.font_name = 'Sprite Comic'
    text_hp_value.font_size = 8

    text_ep = pyglet.text.Label("EP: ", x=20 , y=15, batch=main_batch)
    text_ep.font_name = 'Sprite Comic'
    text_ep.font_size = 8

    text_ep_value = pyglet.text.Label("0", x=460 , y=15, batch=main_batch)
    text_ep_value.font_name = 'Sprite Comic'
    text_ep_value.font_size = 8

    global text_intro
    text_intro = pyglet.text.Label("Press space to start", x=550 , y=400)
    text_intro.font_name = 'Sprite Comic'
    text_intro.anchor_x = "center"
    text_intro.anchor_y = "center"
    text_intro.font_size = 40

def overworld_map_spawn():
    global main_batch

    global unitList
    unitList = []

    global objectList
    objectList = []

    for index in range(26):
        objectList.append(doodads.CastleBlock(main_batch, 0, 125 + index * 25))
        objectList.append(doodads.CastleBlock(main_batch, 900, 125 + index * 25))
        objectList.append(doodads.CastleBlock(main_batch, 1175, 125 + index * 25))

    for index in range(48):
        objectList.append(doodads.CastleBlock(main_batch, index * 25, 100))
        objectList.append(doodads.CastleBlock(main_batch, index * 25, 775))

    global hudHealthBar, hudEnergyBar, hudScreen, hudQIcon, hudWIcon, hudEIcon, hudRIcon, skillTexts
    
    hudScreen = hud.HudFrame(main_batch, 0, 0)
    objectList.append(hudScreen)
    hudHealthBar = hud.HudBar(main_batch, 0, 50, 40)
    hudEnergyBar = hud.HudBar(main_batch, 1, 50, 10)
    hudQIcon = hud.HudIcon(main_batch, 500, 40, 'icon-shuriken.png')
    hudWIcon = hud.HudIcon(main_batch, 560, 40, None)
    hudEIcon = hud.HudIcon(main_batch, 620, 40, None)
    hudRIcon = hud.HudIcon(main_batch, 680, 40, None)
    
    skillTexts = []
    text = pyglet.text.Label("Q", x=520, y=10, batch=main_batch)
    text.font_name = 'Sprite Comic'
    text.font_size = 8
    skillTexts.append(text)

    text = pyglet.text.Label("W", x=580, y=10, batch=main_batch)
    text.font_name = 'Sprite Comic'
    text.font_size = 8
    skillTexts.append(text)

    text = pyglet.text.Label("E", x=640, y=10, batch=main_batch)
    text.font_name = 'Sprite Comic'
    text.font_size = 8
    skillTexts.append(text)

    text = pyglet.text.Label("R", x=700, y=10, batch=main_batch)
    text.font_name = 'Sprite Comic'
    text.font_size = 8
    skillTexts.append(text)



    global testBlock
    testBlock = doodads.CastleBlock(main_batch, 200, 500)
    objectList.append(testBlock)
    global execute
    execute = False

def constants_load():
    global started
    started = False

    global mouseX , mouseY
    mouseX = 0
    mouseY = 0

def overworld_units_spawn():
    global player, main_batch, objectList, enemiesList

    player = units.Ninja(main_batch, 200, 200, 1, objectList)
    objectList.append(player)    

    enemiesList = []
    for index in range(3):
        enemy = units.NinjaMinion(main_batch, 400 + index * 50, 400 + index * 50, 13, objectList)
        enemiesList.append(enemy)
        objectList.append(enemy)

def initialization():
    display_window_preload()
    display_fps_show()
    texture_load_all()
    display_hud()
    overworld_map_spawn()
    overworld_units_spawn()
    constants_load()

############## BEFORE EVENTS ####################
initialization()

@window.event
def on_draw():
    window.clear()
    if started:
        main_batch.draw()
    else:
        text_intro.draw()
    display_fps.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    global player, mouseX, mouseY
    player.on_mouse_press(x, y, button, modifiers)   

@window.event
def on_mouse_release(x, y, button, modifiers):
    pass

@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouseX, mouseY
    mouseX = x
    mouseY = y

@window.event
def on_key_press(symbol, modifiers):
    global player, mouseX, mouseY
    player.on_key_press(symbol, modifiers, mouseX, mouseY)  

    global  started
    if symbol == key.SPACE:
        if not started:
            started = True

@window.event
def on_key_release(symbol, modifiers):
    pass


def assigned(object):
    try:
        object  
        return True
    except:
        return False

def eventSkills(dt):
    global player, enemiesList, objectList, text_hp_Value, text_ep_value, hudHealthBar, hudEnergyBar, hudQIcon

    for object in objectList:
        if object.type == 30:
            if object.opacity < 100:
                object.update(dt)
            else:
                object.text.delete()
                objectList.remove(object)
                del object

    global testBlock
    circle(200, 500, 50, dt)

    hudQIcon.update(player.skillQ.cooldownTime, player.skillQ.cooldown)
    
    playerIsAlive = False
    try:
        player  
        playerIsAlive = True
    except:
        playerIsAlive = False

    if playerIsAlive:
        hudHealthBar.update(player.health, player.healthMax)
        hudEnergyBar.update(player.energy, player.energyMax)

        player.update(dt, objectList)  
        text_hp_value.text = str(int(player.health))
        text_ep_value.text = str(int(player.energy))

        for enemy in enemiesList:
            enemy.moveX = player.sprite.x
            enemy.moveY = player.sprite.y
            enemy.update(dt, objectList)  
            
            if enemy.alive == False:
                objectList.remove(enemy)
                enemiesList.remove(enemy)
                del enemy 

        if player.alive == False:
            objectList.remove(player)
            del player  


def update(dt):
    if started:
        eventSkills(dt)
        
##########################################################################

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0/60)
    pyglet.app.run()
