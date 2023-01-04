import pygame, sys, math
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
P1 = X # the piece player 1 has
P2 = X # the piece player 2 has
CURRENT_TURN = P1 # who is currently playing
P2_CPU = False # is player 2 a computer player or not?

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

    waiting_for_input = True

    # game loop
    while True:
        DISPLAY.fill(WHITE)
        draw_board()

        clicked_button = None

        # START TESTING
        draw_icon(X, 0, 0)
        draw_icon(O, 1, 1)
        draw_icon(X, 2, 2)
        highlight_space(2, 0)
        highlight_space(0, 1)
        highlight_space(1, 2)
        # END TESTING

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mx, my = event.pos
                clicked_button = get_button_clicked(mx, my)
                pass
            elif event.type == KEYDOWN:
                pass

        if waiting_for_input:
            # wait for player to select a square
            if clicked_button:
                pass

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def draw_board():
    """
    Draws an empty board.
    """
    # verticals
    pygame.draw.line(DISPLAY, BLACK, (150, 55), (150, WIN_HEIGHT - 55), 10)
    pygame.draw.line(DISPLAY, BLACK, (250, 55), (250, WIN_HEIGHT - 55), 10)

    # horizontals
    pygame.draw.line(DISPLAY, BLACK, (55, 150), (WIN_WIDTH - 55, 150), 10)
    pygame.draw.line(DISPLAY, BLACK, (55, 250), (WIN_WIDTH - 55, 250), 10)

def draw_icon(icon, x, y):
    """
    Draws 'icon' (x or o) on board coordinates x and y (each ranging from 0-2)
    """
    if board[x][y] != '' and board[x][y] != icon:
        print('ERROR in draw_icon: Can\'t replace icon with different icon')
        return # don't draw over something that isn't the current icon

    if icon == O:
        pygame.draw.circle(DISPLAY, O_COLOR, (100 * (x + 1), 100 * (y + 1)), 25, 5)
    elif icon == X:
        pygame.draw.line(DISPLAY, X_COLOR, (75 + (100 * x), 75 + (100 * y)), (125 + (100 * x), 125 + (100 * y)), 5)
        pygame.draw.line(DISPLAY, X_COLOR, (125 + (100 * x), 75 + (100 * y)), (75 + (100 * x), 125 + (100 * y)), 5)
    board[x][y] = icon

def highlight_space(x, y):
    """
    Highlight square at board coordinates x and y (0-2)
    """
    pygame.draw.rect(DISPLAY, BLUE, pygame.Rect((2 * x + 1) * 50 + 5, (2 * y + 1) * 50 + 5, 91, 91), 10)

def get_button_clicked(x, y):
    """
    Converts window coordinates to board coordinates
    """
    if (x < 55 or x > WIN_HEIGHT - 55) or (y < 50 or y > WIN_HEIGHT - 50):
        return None

    board_x = math.floor((x - 55) / 100)
    board_y = math.floor((y - 50) / 100)
    return board_x, board_y

main()