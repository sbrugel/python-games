# Snake

Originally done by Al Sweigart, this is a Pygame adaptation of Snake.

The player controls a Snake that continuously moves around a gridded board. The player can control its direction, aiming for fruits to increase their score and the snake's length. The goal of the game is to go as long as possible before the snake either runs into itself or into an edge.

![image](https://i.imgur.com/eANwEER.gif)

## Controls

`Arrow keys` - Change snake direction

## Customizability

- Game speed can be normal (15 FPS) or fast (25 FPS)
- Snake body parts added per fruit can be set from 1 to 3
- Disappearing fruits: after 45 ticks (approximately 3 seconds in normal speed), fruits will disappear off the board. If the snake misses 3 fruits, the game automatically ends.
- Color of snake and fruit can be customized

## Other changes from original

- [Change] Initial direction is set to LEFT if player spawns on right half of the board, overall giving the player more time to react. This is different from the original version where the snake always starts facing right.
- [Docs] Function documentation and additional comments added
