import pyglet

class Sound():
    def __init__(self, name):
        self.name = name
        self.file = None

        if self.name == 'slash':
            self.file = pyglet.media.load('game/sounds/slash.wav', streaming=False) 
        elif self.name == 'shuriken':
            self.file = pyglet.media.load('game/sounds/shuriken.wav', streaming=False)   
        elif self.name == 'shield':
            self.file = pyglet.media.load('game/sounds/shield.wav', streaming=False) 
        elif self.name == 'arrow':
            self.file = pyglet.media.load('game/sounds/arrow.wav', streaming=False)
           

class SoundEnchanter():
    def load(self, name, manager):
        result = None

        for sound in manager.sounds:
            if sound.name == name:
                result = sound
        
        if result == None:
            sound = Sound(name)
            manager.sounds.append(sound)
            result = sound

        return result