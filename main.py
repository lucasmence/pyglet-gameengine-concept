import pyglet
pyglet.options['debug_gl'] = False
from pyglet.window import key
from pyglet.window import FPSDisplay
from pyglet.window import mouse
from pyglet import font
from game import textures
from game import units
from game import doodads
from game import hud
from game import managerControl
from game import collision

def circle(x, y, radius, dt):
    global testBlock
    import math
    global execute, i, iterations, c, s, dx, dy
    if not execute:
        execute = True
        iterations = int(2*radius*math.pi) * 0.10
        s = math.sin(2*math.pi / iterations)
        c = math.cos(2*math.pi / iterations) 
        i = 0
        dx, dy = radius, 0

    #for i in range(iterations+1): 
    if i < int(iterations)+1:   
        testBlock.sprite.x = (x + dx)
        testBlock.sprite.y = (y + dy)
        dx, dy = (dx*c - dy*s), (dy*c + dx*s)
        i += 1
    else:
        execute = False
        

def display_window_preload():
    global window
    window = pyglet.window.Window(width=1200, height=800, caption="ardunes-game", resizable=False)
    window.set_location(400, 100)

    global mainBatch
    mainBatch = pyglet.graphics.Batch()

    global manager
    manager = managerControl.Manager(mainBatch)


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

    global text_intro
    text_intro = pyglet.text.Label("Press space to start", x=550 , y=400)
    text_intro.font_name = 'Sprite Comic'
    text_intro.anchor_x = "center"
    text_intro.anchor_y = "center"
    text_intro.font_size = 40

    global mainBatch,  manager
    hudScreen = hud.Hud(mainBatch, player)
    manager.huds.append(hudScreen)
    hudScreen.load(mainBatch)

def overworld_map_spawn():
    global mainBatch,  manager

    for index in range(26):
        manager.doodads.append(doodads.CastleBlock(mainBatch, 0, 125 + index * 25, manager))
        manager.doodads.append(doodads.CastleBlock(mainBatch, 900, 125 + index * 25, manager))
        manager.doodads.append(doodads.CastleBlock(mainBatch, 1175, 125 + index * 25, manager))

    for index in range(48):
        manager.doodads.append(doodads.CastleBlock(mainBatch, index * 25, 100, manager))
        manager.doodads.append(doodads.CastleBlock(mainBatch, index * 25, 775, manager))
    
    global testBlock
    testBlock = doodads.CastleBlock(mainBatch, 200, 500, manager)
    manager.doodads.append(testBlock)
    global execute
    execute = False

def constants_load():
    global started
    started = False

    global mouseX , mouseY
    mouseX = 0
    mouseY = 0

def overworld_units_spawn():
    from game import characters
    global player, mainBatch, enemiesList, manager

    player = characters.Hero(mainBatch, 200, 200, 1, manager)
    manager.units.append(player)    

    enemiesList = []
    
    #for index in range(3):
    #    enemy = characters.SkeletonWarrior(mainBatch, 400 + index * 20, 400 + index * 20, 13, manager)
    #    enemiesList.append(enemy)
    #    manager.units.append(enemy)
    
    
    for index in range(2):
        enemy = characters.SkeletonArcher(mainBatch, 500 + index * 150, 300 + index * 150, 13, manager)
        enemiesList.append(enemy)
        manager.units.append(enemy)
    
    for index in range(1):
        enemy = characters.SkeletonElite(mainBatch, 600 + index * 20, 400 + index * 20, 13, manager)
        enemiesList.append(enemy)
        manager.units.append(enemy)

def initialization():

    display_window_preload()
    display_fps_show()
    overworld_map_spawn()  
    overworld_units_spawn()
    display_hud()
    constants_load()

############## BEFORE EVENTS ####################
initialization()

@window.event
def on_draw():
    window.clear()
    if started:
        mainBatch.draw()
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

def eventSkills(dt):
    global player, enemiesList, manager

    circle(200, 500, 100, dt)
    
    playerIsAlive = False
    try:
        player  
        playerIsAlive = True
    except:
        playerIsAlive = False

    if playerIsAlive:
        manager.update(dt)

        for enemy in enemiesList:
            enemy.angle = collision.angle(player.sprite.x, enemy.sprite.x, player.sprite.y, enemy.sprite.y)
            enemy.moveX = player.sprite.x
            enemy.moveY = player.sprite.y

def update(dt):
    if started:
        eventSkills(dt)
        
##########################################################################

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0/60)
    pyglet.app.run()
