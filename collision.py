import pyglet
import math

def distance(x, y):
    return math.sqrt( ( y * y ) + ( x  * x ) )

def angle(x1, x2, y1, y2):
    angleValue = math.degrees(math.atan2(y1-y2, x1-x2))
    if angleValue < 0:
        angleValue += 360
    return angleValue

def collision(entity, angleUnit, manager):

    for item in manager.units:
        if item.x < entity.x + entity.width and item.x + item.width > entity.x \
                and item.y < entity.y + entity.height and item.height + item.y > entity.y:

            angleDiference = angle(item.x, entity.x, item.y, entity.y) - angleUnit
            if angleDiference < 0:
                angleDiference = angleDiference * -1

            if angleDiference <= 45:
                return True 

def collisionObject(entity, angleUnit, manager):

    for item in manager.doodads:
        if item.sprite.x < entity.sprite.x + entity.sprite.width and item.sprite.x + item.sprite.width > entity.sprite.x \
                and item.sprite.y < entity.sprite.y + entity.sprite.height and item.sprite.height + item.sprite.y > entity.sprite.y:

            if (entity.type == 1):
                angleDiference = angle(item.sprite.y, entity.sprite.y, item.sprite.x, entity.sprite.x) - angleUnit

                if angleDiference < 0:
                    angleDiference = angleDiference * -1              
                if angleDiference <= 35:
                    return 1 
            elif (entity.type == 3):
                return 1
    for item in manager.units:
        if (item.owner != entity.owner):

            if item.sprite.x < entity.sprite.x + (entity.sprite.width * 0.7) and item.sprite.x + (item.sprite.width * 0.7) > entity.sprite.x \
                    and item.sprite.y < entity.sprite.y + (entity.sprite.height * 0.7) and (item.sprite.height * 0.7) + item.sprite.y > entity.sprite.y:
                return item

            if (item.type == 1) and (entity.type == 1):
                distanceX = item.sprite.x - entity.sprite.x
                distanceY = item.sprite.y - entity.sprite.y

                if (distanceX < 0):
                    distanceX = distanceX * -1
                if (distanceY < 0):
                    distanceY = distanceY * -1
                
                distanceTotal = distance(distanceX, distanceY)

                if distanceTotal <= 50:
                    angleDiference = angle(item.sprite.y, entity.sprite.y, item.sprite.x, entity.sprite.x) - angleUnit

                    if angleDiference < 0:
                        angleDiference = angleDiference * -1              
                    if angleDiference <= 60:
                        return 1 
        