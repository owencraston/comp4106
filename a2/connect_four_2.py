import numpy
from random import randint

# set a turn counter
turn = 1

ROW_COUNT = 6
COLUMN_COUNT = 7

game_over = False

def draw_board():
    a = numpy.zeros(shape=(ROW_COUNT, COLUMN_COUNT), dtype=int)
    return a

def is_game_over(response):
    if response == 1:
        return False
    else:
        return True

def random_position():
    x_pos = randint(0, ROW_COUNT-1)
    y_pos = randint(0, COLUMN_COUNT-1)
    return [x_pos, y_pos]

def random_move(board_state):
    move = random_position()
    while board_state.item((move[0], move[1])) != 0:
        move = random_position()
    return move


board = draw_board()
while not game_over:
    # initial load
    if turn == 1:
        print("Welcome to connect four. Connect four of your pieces in a row to win.")
        print("Board size: ", str(ROW_COUNT) + " x " + str(COLUMN_COUNT))
        print("Initial board state: \n", board)

    # handle turn gameplay
    # if the turn is odd play random move
    if turn%2 == 1:
        print("turn 1")
        move = random_move(board)
        print("Random player plays at", move)
        board[move[0], move[1]] = 1
        turn += 1
        # if turn is even play the algorithm
    elif turn%2 == 0:
        print("turn 2")
        move2 = random_move(board)
        print("Ai plays at ", move2)
        board[move2[0], move2[1]] = 2
        turn += 1
    
    # print the baord state after the moves
    print(board)

    # check if the player wants to keep playing
    res = input("Continue plaiyng? Type 1 for yes and anything else to quit. ")
    game_over = is_game_over(int(res))
