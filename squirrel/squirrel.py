class Squirrel():
    x = 0
    y = 0
    width = 0
    height = 0
    movex = 0
    movey = 0
    surface = None
    bounce = 0
    bouncerate = 0
    bounceheight = 0
    
    rect = None

    def __init__(self, x, y, width, height, movex, movey, surface, bounce, bouncerate, bounceheight):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.movex = movey
        self.surface = surface
        self.bounce = bounce
        self.bouncerate = bouncerate
        self.bounceheight = bounceheight