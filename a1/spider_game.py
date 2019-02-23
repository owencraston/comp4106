import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

# init game
screen = curses.initscr()
curses.curs_set(0)
h = 30
w = 70
x, y = 0, 0
w = curses.newwin(h, w, x, y)
w.keypad(1)
w.border(0)
w.nodelay(1)


def spawn_ant(border_choice):
    if (border_choice >= 0 and border_choice <= 3):    
        border = {
            0: [randint(0, 30), 0],
            1: [0, randint(0, 70)],
            2: [randint(0, 30), 69],
            3: [29, randint(0, 70)],
        }
        return border.get(border_choice, [randint(0, 30), 0])
    else:
        raise ValueError('border_choice must be an int value between 0-3.' + border_choice + ' was found')


border_choice = randint(0,3)
ant = spawn_ant(border_choice)
# add the ant to the screen
w.addch(ant[0], ant[1], curses.ACS_DIAMOND)
ant_direction = randint(0,3)


key = KEY_RIGHT

while key != 27:
    # get the next movement 
    prevKey = key
    nextKey = w.getch()
    key = key if nextKey == -1 else nextKey

    # logic for paused game
    if key == ord(' '):                                            
        while key != ord(' '):
            key = w.getch()
        key = prevKey
        continue

    # hanle invalid keys (anything but the arrow keys and escape key)
    if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:
        key = prevKey

