class Grass():
    x = 0
    y = 0
    width = 0
    height = 0
    rect = None

    grassimage = None

    def __init__(self, x, y, width, height, rect, grassimage):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = rect
        self.grassimage = grassimage