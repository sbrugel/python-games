class Ball():
    x = 0
    y = 0
    xvel = 0
    yvel = 0
    rect = None

    def __init__(self, x, y, xvel, yvel, rect):
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.rect = rect