from designer import *
from random import randint, uniform
import math
import sys

set_window_color('black')
enable_keyboard_repeating()

World = {
    'ship': DesignerObject,
    'score': int,
    'score display': DesignerObject,
    'asteroids': [DesignerObject],
    'xvel': float,
    'yvel': float,
    'rot': int,
    'asteroids xvel': [float],
    'asteroids yvel': [float],
    'asteroids rvel': [float],
    'asteroids size': [int],
    'projectiles': [DesignerObject],
    'projectiles xvel': [float],
    'projectiles yvel': [float],
    'bonus': [DesignerObject],
    'bonus xvel': [float],
    'bonus yvel': [float],
    'bonus rvel': [float],
    'particles': [DesignerObject],
    'particles xvel': [float],
    'particles yvel': [float],
    'particles lifetime': [int],
    'over': bool
}

MAX_VEL = 3
ROTATE_RATE = 10
DECEL_RATE = 0.05

'''
Creates the player controlled ship object.

Returns:
    (DesignerObject): The ship
'''
def create_ship() -> DesignerObject:
    ship = image('ship.png')
    ship['scale'] = .75
    return ship

'''
Constantly moves the ship based on its velocity.

Args:
    world (World): The game world
'''
def move_ship(world: World):
    # constantly move ship based on velocity
    world['ship']['x'] += world['xvel']
    world['ship']['y'] += world['yvel']
    
    # wrap around the window if hits the edges
    if world['ship']['x'] < 0:
        world['ship']['x'] = get_width()
    elif world['ship']['x'] > get_width():
        world['ship']['x'] = 0
    # wrap around the window if hits the edges    
    if world['ship']['y'] < 0:
        world['ship']['y'] = get_height()
    elif world['ship']['y'] > get_height():
        world['ship']['y'] = 0

'''
Change velocity of the ship based, rotate, and fire projectiles based on key presses.

Args:
    world (World): The game world
    key (str): The key being pressed
'''
def check_inputs(world: World, key: str):
    # movement to sides - maximum velocity at a time per direction is MAX_VEL units/frame
    if key == 'a':
        world['xvel'] = -MAX_VEL
    if key == 'd':
        world['xvel'] = MAX_VEL
    if key == 'w':
        world['yvel'] = -MAX_VEL
    if key == 's':
        world['yvel'] = MAX_VEL
        
    # launch projectile (if game is not over)
    if key == 'space':
        if not world['over']:
            make_projectile(world)
        
    # change angle of ship using arrows
    if key == 'left':
        world['ship']['angle'] -= ROTATE_RATE
    if key == 'right':
        world['ship']['angle'] += ROTATE_RATE
        
'''
Naturally de-celerate the ship if it is moving.

Args:
    world (World): The game world
'''
def decel(world: World):
    # natural deceleration of ship when rockets are unpowered
    # (ship slows to a stop, does not immediately
    # stop when player lifts up from key)
    if world['xvel'] < 0:
        world['xvel'] += DECEL_RATE
    elif world['xvel'] > 0:
        world['xvel'] -= DECEL_RATE
        
    if world['yvel'] < 0:
        world['yvel'] += DECEL_RATE
    elif world['yvel'] > 0:
        world['yvel'] -= DECEL_RATE
        
'''
Creates an asteroid object.

Returns:
    (DesignerObject): An asteroid object
'''
def create_asteroid() -> DesignerObject:
    asteroid = image('asteroid.png')
    return asteroid

'''
Per frame, run a dice to decide on whether to summon an asteroid. If so, create one and initialize its
x/y velocities, rotation speed and size.

Args:
    world (World): The game world
'''
def make_asteroids(world: World):
    # less than 10 asteroids? create an asteroid    
    not_too_many = len(world['asteroids']) < 10
    
    # 2% chance of asteroid creation per frame (updated 30 times per second)
    dice = randint(0, 50) == 1
    
    # less than too many asteroids and random chance met
    if not_too_many and dice:
        world['asteroids'].append(create_asteroid())
        
        # this line is used to find the newly created asteroid
        # to add a velocity to
        index_created = len(world['asteroids']) - 1
        
        # initialize the asteroid properties
        xvel = 0 # x velocity
        yvel = 0 # y velocity
        rvel = 0 # rotation velocity
        size = 0 # size - small/medium/large corresponds to 1/2/3
        
        # set a random velocity property for this asteroid, making sure
        # all movement velocities are non-zero
        while xvel == 0 and yvel == 0:
            xvel = randint(-3, 3)
            yvel = randint(-3, 3)
            rvel = uniform(-3.0, 3.0)
            size = randint(1, 4)
        
        if xvel < 0:
            world['asteroids'][index_created]['x'] = get_width() - 1
            # going to left, spawn on right
        else:
            world['asteroids'][index_created]['x'] = 1
            # going to right, spawn on left
        
        if size == 1:
            world['asteroids'][index_created]['scale'] = 0.2
        elif size == 2:
            world['asteroids'][index_created]['scale'] = 0.5
        elif size == 3:
            world['asteroids'][index_created]['scale'] = 0.8
        # maintain properties for this asteroid until destroyed
        world['asteroids xvel'].append(xvel)
        world['asteroids yvel'].append(yvel)
        world['asteroids rvel'].append(rvel)
        world['asteroids size'].append(size)
        
'''
Per frame, move all asteroids in the game based on their assigned velocities

Args:
    world (World): The game world
'''
def move_asteroids(world: World):
    if len(world['asteroids']) == 0:
        return # nothing to move
    for i in range(len(world['asteroids'])):
        # move each asteroid based on its assocaited velocity
        world['asteroids'][i]['x'] += world['asteroids xvel'][i]
        world['asteroids'][i]['y'] += world['asteroids yvel'][i]
        world['asteroids'][i]['angle'] += world['asteroids rvel'][i]
        
'''
Create a bonus object

Returns:
    (DesignerObject): A bonus object
'''
def create_bonus() -> DesignerObject:
    bonus = image('coin.png')
    return bonus

'''
Per frame, run a dice to decide on whether to summon a bonus. If so, create one and initialize its
x/y velocities, and rotation speed

Args:
    world (World): The game world
'''
def make_bonus(world: World):
    # only 1 bonus at a time
    not_too_many = len(world['bonus']) < 1
    
    # 2% chance of coin creation per frame (updated 30 times per second)
    dice = randint(0, 50) == 1
    
    # no bonus already exists and random chance met
    if not_too_many and dice:
        world['bonus'].append(create_bonus())
        
        # initialize the bonus properties
        xvel = 0 # x velocity
        yvel = 0 # y velocity
        rvel = 0 # rotation velocity
        
        # set a random velocity property for this bonus, making sure
        # all movement velocities are non-zero
        while xvel == 0 and yvel == 0:
            xvel = randint(-3, 3)
            yvel = randint(-3, 3)
            rvel = uniform(-3.0, 3.0)
        
        if xvel < 0:
            world['bonus'][0]['x'] = get_width() - 1 # going to left, spawn on right
        else:
            world['bonus'][0]['x'] = 1 # going to right, spawn on left
        
        # maintain properties for this bonus until destroyed
        world['bonus xvel'].append(xvel)
        world['bonus yvel'].append(yvel)
        world['bonus rvel'].append(rvel)

'''
Per frame, move all bonuses in the game based on their assigned velocities

Args:
    world (World): The game world
'''
def move_bonus(world: World):
    if len(world['bonus']) == 0:
        return # nothing to move
    for i in range(len(world['bonus'])):
        # move each bonus based on its assocaited velocity
        world['bonus'][i]['x'] += world['bonus xvel'][i]
        world['bonus'][i]['y'] += world['bonus yvel'][i]
        world['bonus'][i]['angle'] += world['bonus rvel'][i]

'''
Create a projectile object

Returns:
    (DesignerObject): A projectile object
'''
def create_projectile() -> DesignerObject:
    proj = image('projectile.png')
    return proj

'''
Summon a projectile based on the player's position and rotation.

Args:
    world (World): The game world
'''
def make_projectile(world: World):
    # only fire one projectile at a time (for now)
    not_too_many = len(world['projectiles']) < 1
    
    # fire, if no projectiles are present
    if not_too_many:
        world['projectiles'].append(create_projectile())
        index_created = len(world['projectiles']) - 1
        
        # set direction of projectile based on ship direction
        radianangle = math.radians(world['ship']['angle'])
        xvel = math.cos(radianangle) * 20
        yvel = math.sin(radianangle) * -20  # negative since on designer,
                                            # a positive y vel means it goes down
        
        world['projectiles'][index_created]['x'] = world['ship']['x']
        world['projectiles'][index_created]['y'] = world['ship']['y']
        world['projectiles'][index_created]['angle'] = world['ship']['angle']
        
        # maintain velocity for this projectile until destroyed
        world['projectiles xvel'].append(xvel)
        world['projectiles yvel'].append(yvel)
        
'''
Per frame, move all projectiles in the game based on their assigned velocities

Args:
    world (World): The game world
'''        
def move_projectiles(world: World):
    if len(world['projectiles']) == 0:
        return # nothing to move
    for i in range(len(world['projectiles'])):
        # move each projectile based on its assocaited velocity
        world['projectiles'][i]['x'] += world['projectiles xvel'][i]
        world['projectiles'][i]['y'] += world['projectiles yvel'][i]

'''
This function checks based on various conditions if any in-game objects should be destroyed.

Args:
    world (World): The game world
'''
def destroy_if_hit(world: World):
    # handle asteroids
    if not len(world['asteroids']) == 0:
        for i in range(len(world['asteroids'])):
            try:
                if (world['asteroids'][i]['x'] < -50 or world['asteroids'][i]['x'] > get_width()+50 or
                    world['asteroids'][i]['y'] < -50 or world['asteroids'][i]['y'] > get_height()+50):
                    # remove the asteroid if it hits the screen edges
                    remove_asteroid_at_index(i, False, world)
                elif colliding(world['asteroids'][i], world['ship']):
                    # remove the asteroid if it hits the ship, split it into chunks,
                    # also destroy ship and game over
                    world['ship']['scale'] = 0
                    remove_asteroid_at_index(i, True, world)
                    world['over'] = True
                else:
                    # remove the asteroid if it hits a projectile; split it into chunks and also
                    # destroy the projectile
                    # check for every projectile, see if it is colliding with any asteroid
                    for j in range(len(world['projectiles'])):
                        if colliding(world['asteroids'][i], world['projectiles'][j]):
                            remove_asteroid_at_index(i, True, world)
                            hide(world['projectiles'][j])
                            world['projectiles'].pop(j)
                            world['projectiles xvel'].pop(j)
                            world['projectiles yvel'].pop(j)
            except IndexError:
                continue # finished iteration through the full list
        
    # handle projectiles
    if not len(world['projectiles']) == 0:
        for i in range(len(world['projectiles'])):
            try:
                # only one case needed here,
                # the other case (when hitting an asteroid)
                # is handled above
                if (world['projectiles'][i]['x'] < 0 or world['projectiles'][i]['x'] > get_width() or
                    world['projectiles'][i]['y'] < 0 or world['projectiles'][i]['y'] > get_height()):
                    # remove the projectile if it hits the screen edges
                    remove_projectile_at_index(i, world)
            except IndexError:
                continue # finished iteration through the full list
    
    # handle bonus
    if len(world['bonus']) == 0:
        return # nothing to remove
    for i in range(len(world['bonus'])):
        try:
            if (world['bonus'][i]['x'] < 0 or world['bonus'][i]['x'] > get_width() or
                world['bonus'][i]['y'] < 0 or world['bonus'][i]['y'] > get_height()):
                # remove the bonus if it hits the screen edges
                remove_bonus_at_index(i, world)
            elif colliding(world['bonus'][i], world['ship']):
                remove_bonus_at_index(i, world)
                world['score'] += 500
        except IndexError:
            continue # finished iteration through the full list
 
'''
Remove the asteroid at a specified index of the asteroid arrays and (if applicable) split larger asteroids into
smaller pieces.

Args:
    world (World): The game world
    index (int): The index of the arrays to remove
    split (bool): If true, larger asteroids will be split into two smaller pieces.
'''
def remove_asteroid_at_index(index: int, split: bool, world: World):
    # remove the asteroid at the specified array index
    # used in tandem with the destroy_if_hit function
    # which iterates through the full list of asteroids
    # and removes every index that is colliding with the edge,
    # a projectile, or the ship
    
    # a boolean toggle also determines if the asteroid should split
    # if true, larger asteroids split into two smaller asteroids and also
    # summon particles upon destroying.
    # this is used when the asteroid is hit by the ship or a projectile
    
    # if the asteroid's size is >1, create two
    # additional asteroids, one size smaller
    if world['asteroids size'][index] > 1 and split:
        for i in range(2): # create two
            world['asteroids'].append(create_asteroid())
            
            # this line is used to find the newly created asteroid
            # to add a velocity to
            index_created = len(world['asteroids']) - 1
            
            xvel = 0
            yvel = 0
            
            while xvel == 0 and yvel == 0:
                xvel = randint(-3, 3)
                yvel = randint(-3, 3)
            
            rvel = world['asteroids rvel'][index]
            size = world['asteroids size'][index] - 1
            
            # spawn at x and y pos of destroyed asteroid
            world['asteroids'][index_created]['x'] = world['asteroids'][index]['x']
            world['asteroids'][index_created]['y'] = world['asteroids'][index]['y']

            if size == 1:
                world['asteroids'][index_created]['scale'] = 0.3
            elif size == 2:
                world['asteroids'][index_created]['scale'] = 0.5
            elif size == 3:
                world['asteroids'][index_created]['scale'] = 0.7
            # maintain properties for this asteroid until destroyed
            world['asteroids xvel'].append(xvel)
            world['asteroids yvel'].append(yvel)
            world['asteroids rvel'].append(rvel)
            world['asteroids size'].append(size)
            
    if split: # only add to score if player hits the asteroids
        world['score'] += 100
        
        # create particles upon destruction if destroyed by not hitting edge
        # number generated increases based on size
        for i in range(world['asteroids size'][index]*12):
            make_particles(world, world['asteroids'][index]['x'], world['asteroids'][index]['y'])
            
    # destroy the asteroid
    hide(world['asteroids'][index])
    world['asteroids'].pop(index)
    world['asteroids xvel'].pop(index)
    world['asteroids yvel'].pop(index)
    world['asteroids rvel'].pop(index)
    world['asteroids size'].pop(index)
    
'''
Create a particle object.

Returns:
    (DesignerObject): A particle object
'''        
def create_particle() -> DesignerObject:
    # create particles for eye candy when an asteroid is destroyed
    part = image('particle.png')
    return part

'''
Summon a particle at a specified x and y location.

Args:
    world (World): The game world
    xloc (float): X position to spawn at
    yloc (float): Y position to spawn at
'''
def make_particles(world: World, xloc: float, yloc: float):
    world['particles'].append(create_particle())
    
    index_created = len(world['particles']) - 1
        
    # set direction of particle randomly
    radianangle = math.radians(randint(0, 360))
    xvel = math.cos(radianangle) * 3
    yvel = math.sin(radianangle) * -3   # negative since on designer,
                                        # a positive y vel means it goes down
    
    # originate particle at specified x/y location
    world['particles'][index_created]['x'] = xloc
    world['particles'][index_created]['y'] = yloc
    world['particles'][index_created]['scale'] = 2
    
    # maintain velocity for this particle until lifetime expires
    world['particles xvel'].append(xvel)
    world['particles yvel'].append(yvel)
    world['particles lifetime'].append(100) # number of ticks before particle destroyed
 
'''
Per frame, move each particle based on its x/y velocity. Also subtract 1 from its lifetime. Delete the particle
once it reaches a lifetime below 0.

Args:
    world (World): The game world
'''
def move_particles(world: World):
    if len(world['particles']) == 0:
        return # nothing to move
    for i in range(len(world['particles'])):
        try:
            # move each particle based on its assocaited velocity
            world['particles'][i]['x'] += world['particles xvel'][i]
            world['particles'][i]['y'] += world['particles yvel'][i]
            world['particles lifetime'][i] -= 1
            if world['particles lifetime'][i] < 0:
                # destroy particles that are on the screen for too long
                hide(world['particles'][i])
                world['particles'].pop(i)
                world['particles xvel'].pop(i)
                world['particles yvel'].pop(i)
                world['particles lifetime'].pop(i)
        except IndexError:
            continue # reached end of list
        
'''
Remove the projectile at a specified index of the projectile arrays.

Args:
    world (World): The game world
    index (int): The index of the arrays to remove
'''    
def remove_projectile_at_index(index: int, world: World):
    # remove the projectile at the specified array index
    # used in tandem with the destroy_if_hit function
    # which iterates through the full list of projectiles
    # and removes every index that is colliding with the edge,
    # or an asteroid
    hide(world['projectiles'][index])
    world['projectiles'].pop(index)
    world['projectiles xvel'].pop(index)
    world['projectiles yvel'].pop(index)

'''
Remove the bonus at a specified index of the bonus arrays.

Args:
    world (World): The game world
    index (int): The index of the arrays to remove
'''   
def remove_bonus_at_index(index: int, world: World):
    # remove the bonus at the specified array index
    # used in tandem with the destroy_if_hit function
    # which iterates through the full list of bonus items
    # and removes every index that is colliding with the edge,
    # or the ship
    hide(world['bonus'][index])
    world['bonus'].pop(index)
    world['bonus xvel'].pop(index)
    world['bonus yvel'].pop(index)
    world['bonus rvel'].pop(index)

'''
Change the score text to display the current score.

Args:
    world (World): The game world
'''   
def update_score(world: World):
    world['score display']['text'] = 'SCORE: ' + str(world['score'])

'''
Check if the game is over

Args:
    world (World): The game world
    
Returns:
    (bool): If the game is over
'''   
def game_is_over(world: World):
    return world['over']

'''
Change the score text to display the final score and a game over message.

Args:
    world (World): The game world
'''   
def flash_game_over(world):
    world['score display']['text'] = "GAME OVER! Score was " + str(world['score'])

'''
Initialize the world on startup.

Returns:
    (World): The game world
'''  
def create_world() -> World:
    return {
        'ship': create_ship(),
        'score': 0,
        'score display': text('white', 'z', 40, get_width() / 2, 25), # center of screen on the top
        'xvel': 0,
        'yvel': 0,
        'rot': 0,
        'asteroids': [],
        'asteroids xvel': [],
        'asteroids yvel': [],
        'asteroids rvel': [],
        'asteroids size': [],
        'projectiles': [],
        'projectiles xvel': [],
        'projectiles yvel': [],
        'bonus': [],
        'bonus xvel': [],
        'bonus yvel': [],
        'bonus rvel': [],
        'particles': [],
        'particles xvel': [],
        'particles yvel': [],
        'particles lifetime': [],
        'over': False
    }

when('starting', create_world)
when('updating', move_ship)
when('typing', check_inputs)
when('updating', decel)
when('updating', make_asteroids)
when('updating', move_asteroids)
when('updating', make_bonus)
when('updating', move_bonus)
when('updating', move_projectiles)
when('updating', update_score)
when('updating', move_particles)
when('updating', destroy_if_hit)
when(game_is_over, flash_game_over)
start()