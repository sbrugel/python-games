class Paddle():
    x = 0
    y = 0
    yvel = 0
    rect = None

    def __init__(self, x, y, yvel, rect):
        self.x = x
        self.y = y
        self.yvel = yvel
        self.rect = rect