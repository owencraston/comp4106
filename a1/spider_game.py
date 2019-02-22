

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

screen = curses.initscr()
curses.curs_set(0)
h, w = 30, 70
x, y = 0, 0
w = curses.newwin(h, w, x, y)
w.keypad(1)
w.border(0)
w.nodelay(1)

ant_x = randint(1, 30) #initial x position of ant
ant_y = randint(1, 70) #initial y position of ant

# create ant object
ant = [ant_x, ant_y]
# add the ant to the screen
w.addch(ant[0], ant[1], curses.ACS_DIAMOND)

key = KEY_RIGHT

while key != 27:
    # get the next movement 
    prevKey = key
    nextKey = w.getch()
    key = key if nextKey == -1 else nextKey

