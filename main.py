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
from game import characters     

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

    for index in range(29):
        manager.doodads.append(doodads.CastleBlock(mainBatch, 0, 50 + index * 25, manager))
        #manager.doodads.append(doodads.CastleBlock(mainBatch, 900, 50 + index * 25, manager))
        manager.doodads.append(doodads.CastleBlock(mainBatch, 1175, 50 + index * 25, manager))

    for index in range(48):
        manager.doodads.append(doodads.CastleBlock(mainBatch, index * 25, 25, manager))
        manager.doodads.append(doodads.CastleBlock(mainBatch, index * 25, 775, manager))
    
    manager.terrain.append(doodads.Terrain('castle-terrain', 25, 50, mainBatch, manager))

def constants_load():
    global started
    started = False

    global mouseX , mouseY
    mouseX = 0
    mouseY = 0

def overworld_units_spawn():
    global player, mainBatch, enemiesList, manager, step

    step = 0

    player = characters.Hero(mainBatch, 200, 200, 1, manager)
    manager.units.append(player)    

    enemiesList = []


    '''
    for index in range(1):
        enemy = characters.Boss(mainBatch, 700 + index * 20, 400 + index * 20, 13, manager)
        enemiesList.append(enemy)
        manager.units.append(enemy)
    '''

   
    
    for index in range(3):
        enemy = characters.SkeletonWarrior(mainBatch, 400 + index * 20, 400 + index * 20, 13, manager)
        enemiesList.append(enemy)
        manager.units.append(enemy)
    
    
    for index in range(2):
        enemy = characters.SkeletonArcher(mainBatch, 500 + index * 150, 300 + index * 150, 13, manager)
        enemiesList.append(enemy)
        manager.units.append(enemy)
    
    for index in range(1):
        enemy = characters.SkeletonElite(mainBatch, 600 + index * 20, 400 + index * 20, 13, manager)
        enemiesList.append(enemy)
        manager.units.append(enemy)
    
    global music

    music = pyglet.media.Player()
    music.queue(pyglet.media.load('game/sounds/stage.wav'))
    music.loop = True
    music.volume = 0.40
    music.queue(pyglet.media.load('game/sounds/boss.wav'))
    music.queue(pyglet.media.load('game/sounds/clear.wav'))

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
    global music
    window.clear()
    if started:
        mainBatch.draw()
        music.play()
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
    global player, enemiesList, manager, step
    
    playerIsAlive = False
    try:
        player  
        playerIsAlive = True
    except:
        playerIsAlive = False

    if playerIsAlive:
        manager.update(dt, mouseX, mouseY)

        for enemy in enemiesList:
            if player.health > 0:
                enemy.angle = collision.angle(player.sprite.x, enemy.sprite.x, player.sprite.y, enemy.sprite.y)
                enemy.moveX = player.sprite.x
                enemy.moveY = player.sprite.y
            if enemy.health <= 0:
                enemiesList.remove(enemy)

    global music  
    if step == 0 and len(enemiesList) == 0:
        step = 1
        music.next_source()
        for index in range(1):
            enemy = characters.Boss(mainBatch, 900 + index * 20, 500 + index * 20, 13, manager)
            enemiesList.append(enemy)
            manager.units.append(enemy)
    elif step == 1 and len(enemiesList) == 0:
        step = 2
        music.loop = False
        music.next_source()   

def update(dt):
    if started:
        eventSkills(dt)
        
##########################################################################

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0/60)
    pyglet.app.run()
