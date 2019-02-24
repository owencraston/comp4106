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

def handle_ant_movement(direction, ant):
    if direction == 0:
        ant[1] += 1
    if direction == 1:
        ant[0] += 1
    if direction == 2:
        ant[1] -=1
    if direction == 3:
        ant[0] -= 1
    return ant



border_choice = randint(0,3)
ant = spawn_ant(border_choice)
# add the ant to the screen
w.addch(ant[0], ant[1], curses.ACS_DIAMOND)
ant_direction = randint(0,3)

# spider
spider = [15, 35] # initial position values
# add the spider to the screen
w.addch(spider[0], spider[1], curses.ACS_PI)

# key = KEY_RIGHT
score = 0

while w.getch() != 27:
    w.timeout(50)
    w.border(0)
    w.addstr(0, 2, 'Score : ' + str(score) + ' ')

    # handle spider movement
    if w.getch() == KEY_RIGHT:
        # remove the previous spider
        w.addch(spider[0], spider[1], ' ')
        # remove the previous ant
        w.addch(ant[0], ant[1], ' ')
        # move accordingly
        spider[1] += 2
        spider[0] -= 1
        # move the ant randomlly
        ant = handle_ant_movement(border_choice, ant)
    if w.getch() == KEY_DOWN:
        # remove the previous spider
        w.addch(spider[0], spider[1], ' ')
        # remove the previous ant
        w.addch(ant[0], ant[1], ' ')
        spider[0] += 1
        # move the ant randomlly
        ant = handle_ant_movement(border_choice, ant)
    if w.getch() == KEY_LEFT:
        # remove the previous spider
        w.addch(spider[0], spider[1], ' ')
        # remove the previous ant
        w.addch(ant[0], ant[1], ' ')
        spider[1] -= 2
        spider[0] -= 1
        # move the ant randomlly
        ant = handle_ant_movement(border_choice, ant)
    if w.getch() == KEY_UP:
        # remove the previous spider
        w.addch(spider[0], spider[1], ' ')
        # remove the previous ant
        w.addch(ant[0], ant[1], ' ')
        spider[0] -= 2
        spider[1] += 1
        # move the ant randomlly
        ant = handle_ant_movement(border_choice, ant)

    # if the ant goes out of bounds 
    if ant[0] >= 30:
        border_choice = randint(0,3)
        ant = spawn_ant(border_choice)
    if ant[0] < 0:
        border_choice = randint(0,3)
        ant = spawn_ant(border_choice)
    if ant[1] >= 70:
        border_choice = randint(0,3)
        ant = spawn_ant(border_choice)
    if ant[1] < 0:
        border_choice = randint(0,3)
        ant = spawn_ant(border_choice)

    # if the spider goes out of bounds, it comes out the other side
    if spider[0] >= 30:
        spider[0] = 1
    if spider[0] < 0:
        spider[0] = 29
    if spider[1] >= 70:
        spider[1] = 1
    if spider[1] < 0:
        spider[1] = 69

    # check if the spider eats the ant 
    if spider == ant:
        score += 1
        border_choice = randint(0,3)
        ant = spawn_ant(border_choice)

    
    # draw ant again
    w.addch(ant[0], ant[1], curses.ACS_DIAMOND)
     # draw spider again
    w.addch(spider[0], spider[1], curses.ACS_PI)

