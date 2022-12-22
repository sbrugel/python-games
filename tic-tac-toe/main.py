import pygame, sys
from pygame.locals import *

WIN_WIDTH = 400
WIN_HEIGHT = 400
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

BG_COLOR = WHITE
LINE_COLOR = BLACK
X_COLOR = RED
O_COLOR = BLUE

X = 'x' # moves first
O = 'o'

board = [['', '', ''], ['', '', ''], ['', '', '']] # 1-2-3, 4-5-6, 7-8-9
"""
1 | 2 | 3
=========
4 | 5 | 6
=========
7 | 8 | 9
"""

def main():
    global FPSCLOCK, DISPLAY, BASIC_FONT, board

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Tic-Tac-Toe')
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', 20)

    # game loop
    while True:
        DISPLAY.fill(WHITE)
        draw_board()
        draw_icon(X, 0, 0)
        draw_icon(O, 1, 0)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def draw_board():
    """
    Draws an empty board.
    """
    # verticals
    pygame.draw.line(DISPLAY, BLACK, (150, 50), (150, WIN_HEIGHT - 50), 10)
    pygame.draw.line(DISPLAY, BLACK, (250, 50), (250, WIN_HEIGHT - 50), 10)

    # horizontals
    pygame.draw.line(DISPLAY, BLACK, (50, 150), (WIN_WIDTH - 50, 150), 10)
    pygame.draw.line(DISPLAY, BLACK, (50, 250), (WIN_WIDTH - 50, 250), 10)

def draw_icon(icon, x, y):
    """
    Draws 'icon' (x or o) on board coordinates x and y (each ranging from 0-2)
    """
    if board[x][y] != '' and board[x][y] != icon:
        # don't draw over something that isn't the current icon
        return

    if icon == O:
        pygame.draw.circle(DISPLAY, O_COLOR, (100 * (x + 1), 100 * (y + 1)), 25, 5)
    elif icon == X:
        pygame.draw.line(DISPLAY, X_COLOR, (75 + (100 * x), 75 + (100 * y)), (125 + (100 * x), 125 + (100 * y)), 5)
        pygame.draw.line(DISPLAY, X_COLOR, (125 + (100 * x), 75 + (100 * y)), (75 + (100 * x), 125 + (100 * y)), 5)
    board[x][y] = icon

main()