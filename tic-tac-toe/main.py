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
SLEEP_TIME = 0

X = 'x' # moves first
O = 'o'
P1 = X # the piece player 1 has
P2 = O # the piece player 2 has
P2_CPU = False # is player 2 a computer player or not?
current_turn = P1 # who is currently playing

board = [['', '', ''], ['', '', ''], ['', '', '']] # 1-2-3, 4-5-6, 7-8-9
"""
1 | 2 | 3
=========
4 | 5 | 6
=========
7 | 8 | 9
"""

def main():
    global FPSCLOCK, DISPLAY, BASIC_FONT, board, current_turn

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Tic-Tac-Toe')
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', 20)

    waiting_for_input = True

    # game loop
    while True:
        events = pygame.event.get()
        if is_board_full(board): # end of game, stick here until we want to play again
            draw_screen_data(board, 'We have a winner!', False)
            for event in events:
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            continue

        waiting_for_input = True

        draw_screen_data(board, 'Player ' + ('1' if current_turn == P1 else '2') + ', it\'s your turn', True)

        if current_turn == P2 and P2_CPU:
            # computer move
            draw_screen_data(board, 'The CPU is making its turn...', False)
            waiting_for_input = False
            current_turn = P1
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            pygame.time.wait(SLEEP_TIME) # slack between turns
            continue

        clicked_button = None

        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mx, my = event.pos
                clicked_button = get_button_clicked(mx, my)
            elif event.type == KEYDOWN:
                # keys 0-8 select a square
                pass

        if waiting_for_input:
            # waiting for player to select a square
            if clicked_button:
                # syntactic sugars
                X_COORD = 0
                Y_COORD = 1
                if not board[clicked_button[X_COORD]][clicked_button[Y_COORD]] == '':
                    print('This square isn\'t empty')
                else:
                    # make the move, advancing turn
                    board[clicked_button[X_COORD]][clicked_button[Y_COORD]] = current_turn # set the piece here to the current player's piece
                    current_turn = P2 if current_turn == P1 else P1
                    draw_screen_data(board, 'Advancing turns...', False)
                    waiting_for_input = False

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        if not waiting_for_input:
            pygame.time.wait(SLEEP_TIME) # slack between turns

def draw_board(board, highlights):
    """
    Draws an empty board firstly, then filling out spaces automatically based on board data
    Also draws box highlights for empty tiles if 'highlights' is True
    """
    # verticals
    pygame.draw.line(DISPLAY, BLACK, (150, 55), (150, WIN_HEIGHT - 55), 10)
    pygame.draw.line(DISPLAY, BLACK, (250, 55), (250, WIN_HEIGHT - 55), 10)

    # horizontals
    pygame.draw.line(DISPLAY, BLACK, (55, 150), (WIN_WIDTH - 55, 150), 10)
    pygame.draw.line(DISPLAY, BLACK, (55, 250), (WIN_WIDTH - 55, 250), 10)

    # draw board data
    for x in range(0, 3):
        for y in range(0, 3):
            if board[x][y]:
                draw_icon(board[x][y], x, y)
            elif highlights:
                highlight_space(x, y)

def draw_screen_data(board, text, highlights):
    """
    Draws the whole game layout from scratch, including text, board, and highlights (if enabled)
    """
    DISPLAY.fill(WHITE)
    turn_surf = BASIC_FONT.render(text, True, BLACK)
    turn_rect = turn_surf.get_rect()
    turn_rect.topleft = (5, WIN_HEIGHT - 25)
    DISPLAY.blit(turn_surf, turn_rect)
    draw_board(board, highlights)

def draw_icon(icon, x, y):
    """
    Draws 'icon' (x or o) on board coordinates x and y (each ranging from 0-2)
    """
    if board[x][y] != '' and board[x][y] != icon:
        print('ERROR in draw_icon: Can\'t replace icon with different icon')
        return

    if icon == O:
        pygame.draw.circle(DISPLAY, O_COLOR, (100 * (x + 1), 100 * (y + 1)), 25, 5)
    elif icon == X:
        pygame.draw.line(DISPLAY, X_COLOR, (75 + (100 * x), 75 + (100 * y)), (125 + (100 * x), 125 + (100 * y)), 5)
        pygame.draw.line(DISPLAY, X_COLOR, (125 + (100 * x), 75 + (100 * y)), (75 + (100 * x), 125 + (100 * y)), 5)

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

def is_board_full(board):
    for x in range(0, 3):
        for y in range(0, 3):
            if not board[x][y]:
                return False
    return True

main()