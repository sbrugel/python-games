# Squirrel Game

Originally done by Al Sweigart

The player controls a small squirrel that must hop around the scrren. There are two game modes for this game (one added by me) that have different goals:
- **Normal mode**: the player must eat smaller squirrels to grow in size. If the player squirrel touches a squirrel larger than them, they lose one health point. The player wins if their squirrel becomes large enough, and loses if their squirrel loses all health points.
- **Survival mode**: touching *any* squirrel will cause the player to lose health. They must avoid all squirrels for as long as possible.

![image](https://i.imgur.com/GoasoTR.gif)

## Controls

`Arrow keys` - Move

## Customizability

- Normal/Survival mode as described above
- Can toggle so squirrels will generally be bigger, increasing difficulty
- Hardcore toggle: 1 health only

## Other changes from original

- [Change] Allow moving in both horizontal and vertical directions at the same time
- [Refactor] Dictionaries for game structures are now separate object files
- [Docs] Function documentation and additional comments added

## Todo
- Add stopwatch for survival time