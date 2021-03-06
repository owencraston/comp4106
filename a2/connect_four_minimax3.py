import numpy as np
import sys
import math
import random

ROW_COUNT = 6
COLUMN_COUNT = 7

RANDOM_PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

EMPTY = 0

def is_game_over(response):
    if response == 1:
        return False
    else:
        return True

def print_board(board):
	print(np.flip(board, 0))

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT), dtype=int)
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def get_score_for_row(window, piece):
	opp_piece = PLAYER_PIECE
	if piece == opp_piece:
		opp_piece = AI_PIECE
	score = 0
	# 3 in a row
	if window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2
	return score

def get_score(board, piece):
	score = 0
	# horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r, :])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += get_score_for_row(window, piece)
	# score vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:, c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += get_score_for_row(window, piece)
	# positive slope diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += get_score_for_row(window, piece)
	# negative slope diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += get_score_for_row(window, piece)

	return score


def is_terminal_node(board):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, math.inf)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -math.inf)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, get_score(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in range(valid_locations + 1):
            if col > valid_locations:
                for i in valid_locations:
                    b_copy = board.copy()
                    drop_from_bottom(b_copy, col)
                    new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            else:
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, AI_PIECE)
                new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value 

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def new_turn(turn):
    turn += 1
    turn = turn % 2
    return turn

def drop_first(board):
    for col in range(COLUMN_COUNT):
        if board.item(0, col) != 0:
            drop_from_bottom(board, col)
            return [0, col]
        

def drop_from_bottom(board, col):
    if board.item(0, col) != 0:
        for r in range(ROW_COUNT-2):
            if r == ROW_COUNT-1:
                board[r][col] = 0
            else:
                board[r][col] = board[r+1][col]


board = create_board()
game_over = False
turn = 0
count = 0


while not game_over:
    # initial load
    if count == 0:
        print("Welcome to connect four. Connect four of your pieces in a row to win.")
        print("Board size: ", str(ROW_COUNT) + " x " + str(COLUMN_COUNT))
        print("Random Player: ", PLAYER_PIECE)
        print("AI Player: ", AI_PIECE)
        print("Initial board state: \n", board)

    # random player
    if turn == RANDOM_PLAYER:
        print("turn 1")
        # if the random value is out of bouds then drop a piece off the bottom
        if count != 0:
            col = random.randint(0, COLUMN_COUNT)
        else:
            col = random.randint(0, COLUMN_COUNT-1)

        if col == COLUMN_COUNT:
            drop = drop_first(board)
            print("dropped", drop)
        elif is_valid_location(board, col):
            row = get_next_open_row(board, col)
            print("Random player plays at", [row, col])
            drop_piece(board, row, col, PLAYER_PIECE)
            if winning_move(board, PLAYER_PIECE):
                print("Player 1 wins. Game over")
                game_over = True
            turn = new_turn(turn)

            
    # ai player
    elif turn == AI and not game_over:				
        col, minimax_score = minimax(board, 4, -math.inf, math.inf, True)
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            print("Ai plays at ", [row, col])
            drop_piece(board, row, col, AI_PIECE)
            if winning_move(board, AI_PIECE):
                print("Player 2 wins. Game over")
                game_over = True
            turn = new_turn(turn)
    # print the baord state after the moves
    print_board(board)
    count += 1
    if game_over == False:
        # check if the player wants to keep playing
        res = input("Continue plaiyng? Type 1 for yes and anything else to quit. ")
        game_over = is_game_over(int(res))
