# Snake

A simple snake game written with pygame.

![alt text](https://github.com/crescat/snake/blob/master/screenshots/title_screen.png "game title")

## Installation

python 3.6.1 or greater is required.

if python is already installed, install pygame by pip:

```bash
$ pip install -U pygame --user
```

See more details [here](https://www.pygame.org/wiki/GettingStarted).


## How to play

Run this line to start the game:
```bash
$ python3 snake.py
```

![alt text](https://github.com/crescat/snake/blob/master/screenshots/foods.gif "different foods")

### Movements

Use arrow keys to control the snake's movement.

### Regular food and special foods

Regular food (white) will extend the length of the snake by 1 cell.
Eating regular food will have a chance to spawn special foods as below.

Vegetable (green) will extend the length of the snake by 3 cell.

Super food (rainbow) will continuously extend the length of the snake within a short period of time.
During this period, speed of the snake will be doubled.

Poison (red) will cut the length of the snake by half.

You can press space any time to pause the game.

### Game over

![alt text](https://github.com/crescat/snake/blob/master/screenshots/game_over.png "game over")

Snake will die if it eats itself or hit the wall. You can press space to restart the game.
