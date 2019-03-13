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

def evaluate_window(window, piece):
	opp_piece = PLAYER_PIECE
	if piece == opp_piece:
		opp_piece = AI_PIECE

	score = 0
	# 3 in a row
	if window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2
	

	# opponent
	# we think the opponent getting 3 in a row is worse
	elif window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4
	return score

def score_position(board, piece):
	score = 0
	# score center pieces favourably
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	# horizontal 4 in a rows
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r, :])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)
		
	# score vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:, c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)
	
	# positive slope diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)
	# negative slope diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score


def is_terminal_node(board):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
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

def new_turn(turn):
    turn += 1
    turn = turn % 2
    return turn

board = create_board()
game_over = False
turn = 0


while not game_over:
    # initial load
    if turn == 0:
        print("Welcome to connect four. Connect four of your pieces in a row to win.")
        print("Board size: ", str(ROW_COUNT) + " x " + str(COLUMN_COUNT))
        print("Random Player: ", PLAYER_PIECE)
        print("AI Player: ", AI_PIECE)
        print("Initial board state: \n", board)

    # random player
    if turn == RANDOM_PLAYER:
        print("turn 1")
        col = random.randint(0, COLUMN_COUNT-1)
        if is_valid_location(board, col):
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
    if game_over == False:
        # check if the player wants to keep playing
        res = input("Continue plaiyng? Type 1 for yes and anything else to quit. ")
        game_over = is_game_over(int(res))
