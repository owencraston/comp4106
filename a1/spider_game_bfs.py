import curses
from random import randint
from copy import deepcopy

height = 25
width = 35



"""
[0, 0]----------------------[0, 15]
|                               |
|                               |    
|                               |
|                               |
|                               |
|                               |
|                               |
|                               |
|                               |
|                               |
|                               |
|                               |
|                               |
|                               |
|                               |
[10, 0]----------------------[10, 15]
"""

# init game
screen = curses.initscr()
curses.curs_set(0)
score = 0
x, y = 10, 10
w = curses.newwin(height, width, x, y)
w.keypad(1)
w.border(0)
w.nodelay(1)

# logic for the game
def spawn_ant(border_choice):
    if (border_choice >= 0 and border_choice <= 3):    
        border = {
            0: [randint(1, height-2), 1],
            1: [1, randint(1, width-2)],
            2: [randint(1, height-2), height-2],
            3: [height-2, randint(1, width-2)],
        }
        return border.get(border_choice, [randint(1, width-1), 1])
    else:
        raise ValueError('border_choice must be an int value between 0-3.' + border_choice + ' was found')

def ant_bounds(a):
    # if the ant goes out of bounds 
    if a[0] >= height-1:
        a = spawn_ant(border_choice)
    if a[0] <= 0:
        a = spawn_ant(border_choice)
    if a[1] >= width-1:
        a = spawn_ant(border_choice)
    if ant[1] <= 0:
        a = spawn_ant(border_choice)
    return a

def spider_bounds(spd):
    # if the spider goes out of bounds, it comes out the other side
    if spd[0] >= height:
        spd[0] = 1
    if spd[0] <= 0:
        spd[0] = height-1
    if spd[1] >= width:
        spd[1] = 1
    if spd[1] <= 0:
        spd[1] = width-1
    return spd


def check_spider_bounds(spd):
    out_of_bounds = False
    # if the spider goes out of bounds, it comes out the other side
    if spd[0] >= height:
        out_of_bounds = True
    if spd[0] <= 0:
        out_of_bounds = True
    if spd[1] >= width:
        out_of_bounds = True
    if spd[1] <= 0:
        out_of_bounds = True
    return out_of_bounds

def check_ant_bounds(a):
    # if the ant goes out of bounds
    out_of_bounds = False
    if a[0] >= height:
        aout_of_bounds = True
    if a[0] <= 0:
        out_of_bounds = True
    if a[1] >= width:
        out_of_bounds = True
    if ant[1] <= 0:
        out_of_bounds = True
    return out_of_bounds

def get_next_ant_move(direction, a):
    if a:
        # check if the ant is out of bounds
        a = ant_bounds(a)
        if direction == 0:
            a[1] += 1
        if direction == 1:
            a[0] += 1
        if direction == 2:
            a[1] -=1
        if direction == 3:
            a[0] -= 1
        # check again
        a = ant_bounds(a)
        return a
    else:
        raise ValueError('a value must be passed for a. %s',  a, ' was found')

def get_next_spider_move(spidy, move):
    if spidy:
        # check the bounds and assign the new value to spidy
        spidy = spider_bounds(spidy)
        # farthest right
        if move == 0:
            spidy[1] += 2
            spidy[0] -= 1
        # furhter up and right
        if move == 1:
            spidy[1] += 1
            spidy[0] -= 2
        # backwords
        if move == 2:
            spidy[0] += 1
        # farthest left
        if move == 3:
            spidy[1] -= 2
            spidy[0] -= 1
        # furhter up and to the left
        if move == 4:
            spidy[1] += 1
            spidy[0] -= 2
        # one left
        if move == 5:
            spidy[1] -= 1
        # one right
        if move == 6:
            spidy[1] += 1
        # side right
        if move == 7:
            spidy[1] += 1
            spidy[0] += 1
        # side left
        if move == 8:
            spidy[1] -= 1
            spidy[0] -= 1
        # check again if the value is out of bounds
        spidy = spider_bounds(spidy)
        return spidy
    else:
        raise ValueError('spidy must contain an x and y position. %s',  spidy, ' was found')


POSSIBLE_MOVES = [0,1, 2, 3, 4, 5, 6, 7, 8]

class Node():
    def __init__(self, state, parent, depth):
        self.state = state
        self.parent = parent
        self.depth = depth

spider = [5, 5]
border_choice = 0
ant = [3, 7]

# draw the initial objects
w.addch(ant[0], ant[1], curses.ACS_DIAMOND)
w.addch(spider[0], spider[1], curses.ACS_PI)

def BFS(spider_state, ant_state):
    goal = False
    initial_node = Node(spider_state, None, 1)
    node_list = [initial_node]
    initial_ant_state = ant_state

    # check if the first two states math
    if spider_state == ant_state:
        goal = True
        return node_list
    while goal == False and len(node_list) != 0:
        e = node_list.pop(0)
        future_ant_state = initial_ant_state
        for i in range(0, e.depth):
            future_ant_state = get_next_ant_move(border_choice, initial_ant_state)
        for move in POSSIBLE_MOVES:
            next_node = Node(None, None, None)
            next_node.state = get_next_spider_move(deepcopy(e.state), move)
            next_node.parent = e
            next_node.depth = e.depth + 1
            if next_node.state == future_ant_state:
                goal = True
                break
            else:
                node_list.append(next_node)
    return node_list


def new_path(initial_spider_state, initial_ant_state):
    nodes = BFS(initial_spider_state, initial_ant_state)
    path = []
    parent = nodes[-1]
    while parent:
        path.insert(0, parent)
        parent = parent.parent
    return path

correct_path = new_path(deepcopy(spider), deepcopy(ant))
    
while w.getch() != 27:
    w.clear()
    w.refresh()
    w.timeout(200)
    w.border(0)
    w.addstr(0, 1, 'Score: ' + str(score) + ' ')
    w.addstr(0, 10, str(len(correct_path)) + ' ')

    if len(correct_path) > 0:
        # get next value in the path
        next_spider_state = correct_path.pop(0)
        spider = next_spider_state.state
        # draw spider
        w.addch(spider[0], spider[1], curses.ACS_PI)
        # get next position of ant
        ant = get_next_ant_move(border_choice, ant)  
        # draw ant
        w.addch(ant[0], ant[1], curses.ACS_DIAMOND)
    else:
        curses.endwin()

curses.endwin()
