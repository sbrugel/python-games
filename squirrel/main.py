import random, sys, time, math, os, pygame
from pygame.locals import *

FPS = 30
WIN_WIDTH = 640
WIN_HEIGHT = 480
HALF_WIN_WIDTH = int(WIN_WIDTH / 2)
HALF_WIN_HEIGHT = int(WIN_HEIGHT / 2)

GRASSCOLOR = (24, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

CAMERASLACK = 90     # how far from the center the squirrel moves before moving the camera
MOVERATE = 9         # how fast the player moves
BOUNCERATE = 6       # how fast the player bounces (large is slower)
BOUNCEHEIGHT = 30    # how high the player bounces
STARTSIZE = 25       # how big the player starts off
WINSIZE = 300        # how big the player needs to be to win
INVULNTIME = 2       # how long the player is invulnerable after being hit in seconds
GAMEOVERTIME = 4     # how long the "game over" text stays on the screen in seconds
MAXHEALTH = 3        # how much health the player starts with

NUM_GRASS = 80        # number of grass objects in the active area
NUM_SQUIRRELS = 30    # number of squirrels in the active area
SQUIRREL_MIN_SPEED = 3 # slowest squirrel speed
SQUIRREL_MAX_SPEED = 7 # fastest squirrel speed
DIR_CHANGE_FREQ = 2    # % chance of direction change per frame
LEFT = 'left'
RIGHT = 'right'

"""
This program has three data structures to represent the player, enemy squirrels, and grass background objects. The data structures are dictionaries with the following keys:

Keys used by all three data structures:
    'x' - the left edge coordinate of the object in the game world (not a pixel coordinate on the screen)
    'y' - the top edge coordinate of the object in the game world (not a pixel coordinate on the screen)
    'rect' - the pygame.Rect object representing where on the screen the object is located.
Player data structure keys:
    'surface' - the pygame.Surface object that stores the image of the squirrel which will be drawn to the screen.
    'facing' - either set to LEFT or RIGHT, stores which direction the player is facing.
    'size' - the width and height of the player in pixels. (The width & height are always the same.)
    'bounce' - represents at what point in a bounce the player is in. 0 means standing (no bounce), up to BOUNCERATE (the completion of the bounce)
    'health' - an integer showing how many more times the player can be hit by a larger squirrel before dying.
Enemy Squirrel data structure keys:
    'surface' - the pygame.Surface object that stores the image of the squirrel which will be drawn to the screen.
    'movex' - how many pixels per frame the squirrel moves horizontally. A negative integer is moving to the left, a positive to the right.
    'movey' - how many pixels per frame the squirrel moves vertically. A negative integer is moving up, a positive moving down.
    'width' - the width of the squirrel's image, in pixels
    'height' - the height of the squirrel's image, in pixels
    'bounce' - represents at what point in a bounce the player is in. 0 means standing (no bounce), up to BOUNCERATE (the completion of the bounce)
    'bouncerate' - how quickly the squirrel bounces. A lower number means a quicker bounce.
    'bounceheight' - how high (in pixels) the squirrel bounces
Grass data structure keys:
    'grassimage' - an integer that refers to the index of the pygame.Surface object in GRASSIMAGES used for this grass object
"""

dir_path = os.path.dirname(os.path.realpath(__file__)) # the file currently being ran (mainmenu.py)

def main():
    global FPSCLOCK, DISPLAY, BASICFONT, L_SQUIR_IMG, R_SQUIR_IMG, GRASSIMAGES

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_icon(pygame.image.load(dir_path + '/assets/gameicon.png'))
    DISPLAY = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Squirrel Game')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 32)

    # load images
    L_SQUIR_IMG = pygame.image.load(dir_path + '/assets/squirrel.png')
    R_SQUIR_IMG = pygame.transform.flip(L_SQUIR_IMG, True, False) # flip x (True) but not y (False)
    GRASSIMAGES = []
    for i in range(1, 5):
        GRASSIMAGES.append(pygame.image.load(dir_path + '/assets/grass%s.png' % i))

    while True:
        run_game()

def run_game():
    # vars for start of a new game
    invulnerable = False # is player invinsible?
    invulnerable_start_time = 0 # when the player gained invulnerability
    game_over = False # if player lost
    game_over_start_time = 0 # when the player lost
    win_mode = False # did player win?

    # create surfaces to hold game text
    game_over_surf = BASICFONT.render('Game Over', True, WHITE)
    game_over_rect = game_over_surf.get_rect()
    game_over_rect.center = (HALF_WIN_WIDTH, HALF_WIN_HEIGHT)

    win_surf = BASICFONT.render('You won!', True, WHITE)
    win_rect = win_surf.get_rect()
    win_rect.center = (HALF_WIN_WIDTH, HALF_WIN_HEIGHT)

    win_surf2 = BASICFONT.render('Press R to restart', True, WHITE)
    win_rect2 = win_surf2.get_rect()
    win_rect2.center = (HALF_WIN_WIDTH, HALF_WIN_HEIGHT + 30)

    # camera view
    camerax = 0
    cameray = 0

    grass_objs = []
    squirrel_objs = []

    # the player
    player_obj = {'surface': pygame.transform.scale(L_SQUIR_IMG, (STARTSIZE, STARTSIZE)),
                 'facing': LEFT,
                 'size': STARTSIZE,
                 'x': HALF_WIN_WIDTH,
                 'y': HALF_WIN_HEIGHT,
                 'bounce':0,
                 'health': MAXHEALTH}

    m_left = m_right = m_up = m_down = False

    # add some grass
    for i in range(10):
        grass_objs.append(make_new_grass(camerax, cameray))
        grass_objs[i]['x'] = random.randint(0, WIN_WIDTH)
        grass_objs[i]['y'] = random.randint(0, WIN_HEIGHT)
        
    # main loop
    while True:
        # turn off invinsibility?
        if invulnerable and time.time() - invulnerable_start_time > INVULNTIME:
            invulnerable = False

        # move squirrels
        for s in squirrel_objs:
            # move squirrel and adjust for bounce
            s['x'] += s['movex']
            s['y'] += s['movey']
            s['bounce'] += 1

            if s['bounce'] > s['bouncerate']:
                s['bounce'] = 0 # reset bounce

            # random chance of changing direction
            if random.randint(0, 99) < DIR_CHANGE_FREQ:
                s['movex'] = get_random_velocity()
                s['movey'] = get_random_velocity()
                if s['movex'] > 0: # faces right
                    s['surface'] = pygame.transform.scale(R_SQUIR_IMG, (s['width'], s['height']))
                else: # faces left
                    s['surface'] = pygame.transform.scale(L_SQUIR_IMG, (s['width'], s['height']))   
        
        # check if deleting is needed, aka anything is off camera
        for i in range(len(grass_objs) - 1, -1, -1):
            if is_outside_active_area(camerax, cameray, grass_objs[i]):
                del grass_objs[i]
        for i in range(len(squirrel_objs) - 1, -1, -1):
            if is_outside_active_area(camerax, cameray, squirrel_objs[i]):
                del squirrel_objs[i]

        # if we don't have enough, add more grass and squirrels
        while len(grass_objs) < NUM_GRASS:
            grass_objs.append(make_new_grass(camerax, cameray))
        while len(squirrel_objs) < NUM_SQUIRRELS:
            squirrel_objs.append(make_new_squirrel(camerax, cameray))

        # adjust camerax and cameray if beyond the "camera slack"
        player_center_x = player_obj['x'] + int(player_obj['size'] / 2)
        player_center_y = player_obj['y'] + int(player_obj['size'] / 2)
        if (camerax + HALF_WIN_WIDTH) - player_center_x > CAMERASLACK:
            camerax = player_center_x + CAMERASLACK - HALF_WIN_WIDTH
        elif player_center_x - (camerax + HALF_WIN_WIDTH) > CAMERASLACK:
            camerax = player_center_x - CAMERASLACK - HALF_WIN_WIDTH
        if (cameray + HALF_WIN_HEIGHT) - player_center_y > CAMERASLACK:
            cameray = player_center_y + CAMERASLACK - HALF_WIN_HEIGHT
        elif player_center_y - (cameray + HALF_WIN_HEIGHT) > CAMERASLACK:
            cameray = player_center_y - CAMERASLACK - HALF_WIN_HEIGHT

        # now to draw things
        DISPLAY.fill(GRASSCOLOR) # background always goes first

        # grass
        for g in grass_objs:
            g_rect = pygame.Rect((g['x'] - camerax,
                                  g['y'] - cameray,
                                  g['width'],
                                  g['height']))
            DISPLAY.blit(GRASSIMAGES[g['grassimage']], g_rect)

        # other squirrels
        for s in squirrel_objs:
            s['rect'] = pygame.Rect((s['x'] - camerax,
                                     s['y'] - cameray - get_bounce_amount(s['bounce'], s['bouncerate'], s['bounceheight']),
                                     s['width'],
                                     s['height']))
            DISPLAY.blit(s['surface'], s['rect'])

        # the player
        flash_on = round(time.time(), 1) * 10 % 2 == 1
        if not game_over and not (invulnerable and flash_on):
            player_obj['rect'] = pygame.Rect((player_obj['x'] - camerax,
                                              player_obj['y'] - cameray - get_bounce_amount(player_obj['bounce'], BOUNCERATE, BOUNCEHEIGHT),
                                              player_obj['size'],
                                              player_obj['size']))
            DISPLAY.blit(player_obj['surface'], player_obj['rect'])

        # draw health
        draw_health_meter(player_obj['health'])
        
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()

            elif event.type == KEYDOWN:
                if event.key in (K_UP, K_w):
                    m_down = False
                    m_up = True
                elif event.key in (K_DOWN, K_s):
                    m_up = False
                    m_down = True
                elif event.key in (K_LEFT, K_a):
                    m_right = False
                    m_left = True
                    if player_obj['facing'] != LEFT: # change player image
                        player_obj['surface'] = pygame.transform.scale(L_SQUIR_IMG, (player_obj['size'], player_obj['size']))
                    player_obj['facing'] = LEFT
                elif event.key in (K_RIGHT, K_d):
                    m_left = False
                    m_right = True
                    if player_obj['facing'] != RIGHT: # change player image
                        player_obj['surface'] = pygame.transform.scale(R_SQUIR_IMG, (player_obj['size'], player_obj['size']))
                    player_obj['facing'] = RIGHT
                elif win_mode and event.key == K_r:
                    return # start a new game

            elif event.type == KEYUP:
                # stop moving the player's squirrel
                if event.key in (K_LEFT, K_a):
                    m_left = False
                elif event.key in (K_RIGHT, K_d):
                    m_right = False
                elif event.key in (K_UP, K_w):
                    m_up = False
                elif event.key in (K_DOWN, K_s):
                    m_down = False

                elif event.key == K_ESCAPE:
                    terminate()

        if not game_over:
            # move player if moving
            if m_left:
                player_obj['x'] -= MOVERATE
            elif m_right:
                player_obj['x'] += MOVERATE
                
            if m_up:
                player_obj['y'] -= MOVERATE
            elif m_down:
                player_obj['y'] += MOVERATE

            if (m_left or m_right or m_up or m_down) or player_obj['bounce'] != 0:
                player_obj['bounce'] += 1

            if player_obj['bounce'] > BOUNCERATE:
                player_obj['bounce'] = 0 # reset

            # check if collided with any squirrels
            for i in range(len(squirrel_objs)-1, -1, -1):
                s = squirrel_objs[i]
                if 'rect' in s and player_obj['rect'].colliderect(s['rect']):
                    # collision has occurred

                    if s['width'] * s['height'] <= player_obj['size']**2:
                        # player is larger and eats the squirrel
                        player_obj['size'] += int( (s['width'] * s['height'])**0.2 ) + 1
                        del squirrel_objs[i]

                        if player_obj['facing'] == LEFT:
                            player_obj['surface'] = pygame.transform.scale(L_SQUIR_IMG, (player_obj['size'], player_obj['size']))
                        if player_obj['facing'] == RIGHT:
                            player_obj['surface'] = pygame.transform.scale(R_SQUIR_IMG, (player_obj['size'], player_obj['size']))

                        if player_obj['size'] > WINSIZE:
                            win_mode = True # turn on "win mode"

                    elif not invulnerable:
                        # player is smaller and takes damage
                        invulnerable = True
                        invulnerable_start_time = time.time()
                        player_obj['health'] -= 1
                        if player_obj['health'] == 0:
                            game_over = True # turn on "game over mode"
                            game_over_start_time = time.time()
        else:
            # game over
            DISPLAY.blit(game_over_surf, game_over_rect)
            if time.time() - game_over_start_time > GAMEOVERTIME:
                return # end the game

        # check if win
        if win_mode:
            DISPLAY.blit(win_surf, win_rect)
            DISPLAY.blit(win_surf2, win_rect2)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def draw_health_meter(health):
    for i in range(health): # draw red health bars
        pygame.draw.rect(DISPLAY, RED, (15, 5 + (10 * MAXHEALTH) - i * 10, 20, 10))
    for i in range(MAXHEALTH): # outlines
        pygame.draw.rect(DISPLAY, WHITE, (15, 5 + (10 * MAXHEALTH) - i * 10, 20, 10), 1)

def terminate():
    pygame.quit()
    sys.exit()

def get_bounce_amount(current, rate, height):
    """
    Returns number of pixels to offset based on bounce. A larger 'rate' means a slower bounce. A larger 'height' means a higher bounce.
    'current' must always be less than 'rate'
    """
    return int(math.sin((math.pi / float(rate)) * current) * height)

def get_random_velocity():
    speed = random.randint(SQUIRREL_MIN_SPEED, SQUIRREL_MAX_SPEED)
    if random.randint(0, 1) == 0:
        return speed
    else:
        return -speed

def get_random_off_camera_pos(camerax, cameray, obj_width, obj_height):
    # creat rect of camera view
    camera_rect = pygame.Rect(camerax, cameray, WIN_WIDTH, WIN_HEIGHT)
    while True:
        x = random.randint(camerax - WIN_HEIGHT, camerax + (2 * WIN_WIDTH))
        y = random.randint(cameray - WIN_HEIGHT, cameray + (2 * WIN_HEIGHT))
        # create Rect with random coords, use colliderect() to make sure right edge isn't within the camera
        obj_rect = pygame.Rect(x, y, obj_width, obj_height)
        if not obj_rect.colliderect(camera_rect):
            return x, y

def make_new_squirrel(camerax, cameray):
    sq = {} # blank dictionary
    general_size = random.randint(5, 25)
    multiplier = random.randint(1, 3)
    sq['width']  = (general_size + random.randint(0, 10)) * multiplier
    sq['height'] = (general_size + random.randint(0, 10)) * multiplier
    sq['x'], sq['y'] = get_random_off_camera_pos(camerax, cameray, sq['width'], sq['height'])
    sq['movex'] = get_random_velocity()
    sq['movey'] = get_random_velocity()
    if sq['movex'] < 0: # facing left
        sq['surface'] = pygame.transform.scale(L_SQUIR_IMG, (sq['width'], sq['height']))
    else:
        sq['surface'] = pygame.transform.scale(R_SQUIR_IMG, (sq['width'], sq['height']))
    sq['bounce'] = 0
    sq['bouncerate'] = random.randint(10, 18)
    sq['bounceheight'] = random.randint(10, 50)
    return sq

def make_new_grass(camerax, cameray):
    gr = {}
    gr['grassimage'] = random.randint(0, len(GRASSIMAGES) - 1)
    gr['width']  = GRASSIMAGES[0].get_width()
    gr['height'] = GRASSIMAGES[0].get_height()
    gr['x'], gr['y'] = get_random_off_camera_pos(camerax, cameray, gr['width'], gr['height'])
    gr['rect'] = pygame.Rect( (gr['x'], gr['y'], gr['width'], gr['height']) )
    return gr

def is_outside_active_area(camerax, cameray, obj):
    # false if camerax and cameray are more than a half-window length beyond the edge of the window
    left_bound = camerax - WIN_WIDTH
    top_bound = cameray - WIN_HEIGHT
    bounds_rect = pygame.Rect(left_bound, top_bound, WIN_WIDTH * 3, WIN_HEIGHT * 3)
    obj_rect = pygame.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
    return not bounds_rect.colliderect(obj_rect)

main()