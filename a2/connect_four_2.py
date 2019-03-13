import numpy
from random import randint
from math import inf as infinity

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

def _has_tile_in_column(board, column):
    for i in range(ROW_COUNT):
        if board.item(i, column) != 0:
            # return x position
            return i
    # return -1 if that column in empty
    return -1

def random_move(board_state):
    y_pos = randint(0, COLUMN_COUNT-1)
    column_state = _has_tile_in_column(board_state, y_pos)
    if column_state == -1:
        move = [ROW_COUNT-1, y_pos]
    else:
        move = [column_state-1, y_pos]
    return move

def _four_in_a_row_horz(board_state, player):
    count = 0
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            if board_state.item(row, col) == player:
                count += 1
            else:
                count = 0
            if count == 4:
                return True
    return False

def _four_in_a_row_vert(board_state, player):
    count = 0
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            if board_state.item(row, col) == player:
                count += 1
            else:
                count = 0
            if count == 4:
                return True
    return False

def _four_in_a_row_diag(board_state, player):
    # numpy way of getting list of diagonal rows
    # gett the diags from top left to bottom right
    diags = [board_state[::-1,:].diagonal(i) for i in range(-board_state.shape[0]+1, board_state.shape[1])]
    # get diags from top right to bottom left
    diags.extend(board_state.diagonal(i) for i in range(board_state.shape[1]-1,-board_state.shape[0],-1))
    # for the arrays of diagonals in the list...
    for diag in diags:
        # reset count for each one
        count = 0
        # run through the array
        for i in range(len(diag)):
            if diag.item(i) == player:
                count += 1
            else:
                count = 0
            if count == 4:
                return True
    return False

def has_won(board_state, player):
    if _four_in_a_row_horz(board_state, player) == True:
        return True
    if _four_in_a_row_vert(board_state, player) == True:
        return True
    if _four_in_a_row_diag(board_state, player) == True:
        return True
    return False

def __in_the_middle_horz(board_state, player):
    score = 0
    count = 0
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            if board_state.item(row, col) == player:
                count += 1
            else:
                count = 0
            if count == 3:
                score +=1
    return score

def __in_the_middle_vert(board_state, player):
    score = 0
    count = 0
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            if board_state.item(row, col) == player:
                count += 1
            else:
                count = 0
            if count == 3:
                score += 1
    return score

def __in_the_middle_diag(board_state, player):
    score = 0
    # numpy way of getting list of diagonal rows
    # gett the diags from top left to bottom right
    diags = [board_state[::-1,:].diagonal(i) for i in range(-board_state.shape[0]+1, board_state.shape[1])]
    # get diags from top right to bottom left
    diags.extend(board_state.diagonal(i) for i in range(board_state.shape[1]-1,-board_state.shape[0],-1))
    # for the arrays of diagonals in the list...
    for diag in diags:
        # reset count for each one
        count = 0
        # run through the array
        for i in range(len(diag)):
            if diag.item(i) == player:
                count += 1
            else:
                count = 0
            if count == 3:
                score += 1
    return score

def _heuristic1(board_state, player):
    """
    we want to reward the player for having a piece in the middle of two other pieces.
    this is basically checking if there are 3 in a row of a certain players pieces
    """
    score = 0
    score += __in_the_middle_vert(board_state, player)
    score += __in_the_middle_horz(board_state, player)
    score += __in_the_middle_diag(board_state, player)
    return score

def minimax(board_state, depth, player):
    return []
    

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
        if has_won(board, 1) == True:
            print("Player 1 wins. Game over")
            game_over = True
        turn += 1
        # if turn is even play the algorithm
    elif turn%2 == 0:
        print("turn 2")
        move2 = random_move(board)
        print("Ai plays at ", move2)
        board[move2[0], move2[1]] = 2
        if has_won(board, 2) == True:
            print("Player 2 wins. Game over")
            game_over = True
        turn += 1
    
    # print the baord state after the moves
    print(board)
    if game_over == False:
        # check if the player wants to keep playing
        res = input("Continue plaiyng? Type 1 for yes and anything else to quit. ")
        game_over = is_game_over(int(res))
