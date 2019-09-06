import pyglet

class Model():

    def __init__(self):
        pass


class Animation():
    def __init__(self):
        self.time = []
        self.timeMax = []
        self.imageList = []
        self.index = 0
        self.indexCount = 0
        self.sprite = None
    

    def animate(self, sprite, image, timeMax):
        self.sprite = sprite
        self.sprite.image = image[0]
        self.imageList = image
        self.timeMax = timeMax
        self.index = 0
        self.indexCount = len(image) - 1
        self.time = []
        for time in self.timeMax:
            self.time.append(0)

    def update(self, dt):

        result = False

        if self.index <= self.indexCount and len(self.imageList) > 0:
            if self.time[self.index] < self.timeMax[self.index]:
                self.time[self.index] += 1 * dt 
            elif self.index < self.indexCount:
                self.index += 1
                self.sprite.image = self.imageList[self.index]
            else:
                result = True
        else:
            result = True

        return result

class AnimationSprite():
    def __init__(self, sprite, time, name):
        self.sprite = sprite
        self.time = time
        self.name = name

class AnimationManager():
    def __init__(self, sprite):
        self.animationList = []
        self.currentAnimation = ''

        self.animationExecute = Animation()
        self.sprite = sprite

    def animate(self, name, angle):
        
        if (name != 'stand') and (name != 'death'):
            if ((angle >= 0) and (angle <= 90)) or ((angle > 240) and (angle <= 360)):
                name = name + '-right'
            #elif (angle > 60) and (angle <= 120):
            #    name = name + '-up'
            elif (angle > 90) and (angle <= 240):
                name = name + '-left'    
            #elif (angle > 240) and (angle <= 300):
            #    name = name + '-down'

        if (self.currentAnimation != name):
            for animation in self.animationList:
                if animation.name == name: 
                    self.currentAnimation = name
                    self.animationExecute.animate(self.sprite, animation.sprite, animation.time)
                    
        
    def update(self, dt):
        if self.animationExecute.update(dt) == True:
            self.currentAnimation = ''
            self.animate('stand', 0)