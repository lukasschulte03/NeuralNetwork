

posX = 0
posY = 0
velX = 0
velY = 0
accX = 0
accY = 0

accForce = 1

while True:
    velX += accX
    velY += accY
    posX += velX
    posY += velY