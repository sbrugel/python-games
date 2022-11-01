# Python Games

Some games I made/re-created in Python, using the [designer.py](https://designer-edu.github.io/designer/quickstart/quickstart.html#shapes) library (primarily).

## Asteroids

_(1 player only)_

A recreation of the classic Atari game "Asteroids" in Python. This was originally made as my final project for CISC 108 at the University of Delaware, but it has been modified to work with the most recent version of Designer (at the time of writing, `0.4.1` is the current version). I made the visuals of this somewhat true to the original version, having recreated the original 1970s game's sprites.

### About

The player controls a spaceship (represented by an arrow) by rotating and moving it around the map. To score points, they must shoot at asteroids using the `SPACE` key, as well as run into bonus items (yellow boxes). The game ends when the player is killed by colliding with an asteroid.

### Notable Features

- Player controllable spaceship (rotation and movement), with low friction for movement meaning it will slowly come to a stop after a movement key is pressed.
- The player wraps around the map if they hit an edge.
- Asteroids of varying sizes periodically spawn; larger ones split into two smaller asteroids. Particles spawn when an asteroid is hit, moving in a radial direction from the site of destruction.

### Controls

`W` - Move up
`A` - Move left
`S` - Move down
`D` - Move right
`<-` - Rotate anti-clockwise
`->` - Rotate clockwise
`SPACE` - Fire projectile
