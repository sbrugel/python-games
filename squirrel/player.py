class Player():
    x = 0
    y = 0
    surface = None
    facing = None
    size = None
    bounce = 0
    health = 0

    def __init__(self, x, y, surface, facing, size, bounce, health):
        self.x = x
        self.y = y
        self.surface = surface
        self.facing = facing
        self.size = size
        self.bounce = bounce
        self.health = health