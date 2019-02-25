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

def get_next_move(spidy, key):
    # get next move based on key
    if key == KEY_RIGHT:
        spidy[1] += 2
        spidy[0] -= 1
    if key == KEY_DOWN:
        spidy[0] += 1
    if key == KEY_LEFT:
        spidy[1] -= 2
        spidy[0] -= 1
    if key== KEY_UP:
        spidy[0] -= 2
        spidy[1] += 1
    else:
        return spidy

def BFS(spider_state, ant_state):
    # set true when final state is true
    goal = False
    # count the number of moves it takes
    move_count = 0
    # get the initial state
    node_list = [spider_state]
    # while the goal has not been reached and the nodelist isnt empty
    while goal == False or len(node_list) == 0:
        # take the first element from the node list
        e = node_list.pop(0)
        # check if the list is empty
        if len(node_list) == 0:
            break
        # check every option 
        for key in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN]:
            # increment the move counter
            move_count +=1
            # use the helper function to get the next move for the spider
            next_move = get_next_move(e, key)
            # get the next move for the ant
            ant_state = handle_ant_movement(border_choice, ant_state)
            # if the ant and spider are the same (coordinates) the goal has been reached
            if next_move == ant_state:
                goal = True
            else:
                # append this state to the back of the list
                node_list.append(e)
    return node_list

# random test path for the ui
path = [[15, 12], [20, 19], [25, 25], [10, 15], [17, 23], [26, 60]]

while w.getch() != 27:
    w.timeout(50)
    w.border(0)
    w.addstr(0, 2, 'Score : ' + str(score) + ' ')

    if len(path) != 0:
        # remove the previous spider
        w.addch(spider[0], spider[1], ' ')
        # remove the previous ant
        w.addch(ant[0], ant[1], ' ')
        # move accordingly
        spider = path.pop(0)

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

