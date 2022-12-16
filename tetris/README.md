# Tetris

Originally done by Al Sweigart, this is a Pygame adaptation of Tetris.

Blocks of different shapes fall from the top of the screen - the player must guide these down to form rows filled with boxes, void of any gaps. When a complete row is formed, it is cleared and each row above moves down one row. The goal is to complete as many of these lines as possible until the screen fills up.

![image](https://i.imgur.com/7pQWi7j.gif)

## Controls

`Q` - Rotate left
`W` - Rotate right
`Left / Right` - Move block sideways
`Down` - Increase fall speed
`Space` - Automatically drop as far down as possible

## Customizability

- "Ghost pieces" can be toggled, that is, while controlling a piece, a "preview" of how far down it can go is shown on the screen, making it easier to align pieces as desired.
- Falling speed increase per level can be adjusted
- Board size can be changed from a height of 20, down to as little as 10

## Other changes from original

- [Change] Speed increases for every 5 rows complete, not every 10
- [Docs] Function documentation and additional comments added
