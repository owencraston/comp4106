from random import randint
from copy import deepcopy


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

def ant_bounds(a):
    # if the ant goes out of bounds 
    if a[0] >= 30:
        a = spawn_ant(randint(0,3))
    if a[0] < 0:
        a = spawn_ant(randint(0,3))
    if a[1] >= 70:
        a = spawn_ant(randint(0,3))
    if ant[1] < 0:
        a = spawn_ant(randint(0,3))
    return a

def spider_bounds(spd):
    # if the spider goes out of bounds, it comes out the other side
    if spd[0] >= 30:
        spd[0] = 1
    if spd[0] < 0:
        spd[0] = 29
    if spd[1] >= 70:
        spd[1] = 1
    if spd[1] < 0:
        spd[1] = 69
    return spd

def get_next_ant_move(direction, a):
    if a:
        # check if the ant is out of bounds
        a = ant_bounds(a)
        if direction == 0:
            ant[1] += 1
        if direction == 1:
            ant[0] += 1
        if direction == 2:
            ant[1] -=1
        if direction == 3:
            ant[0] -= 1
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
            spidy[1] -= 1
        # side right
        if move == 7:
            spidy[1] += 1
            spidy[0] += 1
        # side left
        if move == 8:
            spidy[1] -= 1
            spidy[0] -= 1
        else:
            # if no valid direction was given
            return spidy
    else:
        raise ValueError('spidy must contain an x and y position. %s',  spidy, ' was found')


POSSIBLE_MOVES = [0,1, 2, 3, 4, 5, 6, 7, 8]

class Node():
    def __init__(self, state, parent, depth):
        self.state = state
        self.parent = parent
        self.depth = depth

spider = [15, 35]
ant = [20, 10]
border_choice = randint(0,3)

def DFS(spider_state, ant_state):
    goal = False
    count = 0
    initial_node = Node(spider_state, None, 0)
    node_list = [initial_node]
    initial_ant_state = ant_state
    while goal == False or len(node_list) == 0:
        e = node_list.pop(0)
        future_ant_state = initial_ant_state
        for i in range(0, e.depth):
            future_ant_state = get_next_ant_move(border_choice, initial_ant_state)

