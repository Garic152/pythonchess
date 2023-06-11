import numpy as np
import time

white, black = range(2)

#source with explanation for the scores
#https://www.chessprogramming.org/Simplified_Evaluation_Function

piece_values = np.array([0, 100, 320, 330, 500, 900, 20000, -100, -320, -330, -500, -900, -20000, 0])

#was using list(reversed(array)) to reverse the array
board_positions = np.array([
    [0,  0,  0,  0,  0,  0,  0,  0,  1,2,3,4,5,6,7,8,
    50, 50, 50, 50, 50, 50, 50, 50, 1,2,3,4,5,6,7,8,
    10, 10, 20, 30, 30, 20, 10, 10, 1,2,3,4,5,6,7,8,
     5,  5, 10, 25, 25, 10,  5,  5, 1,2,3,4,5,6,7,8,
     0,  0,  0, 20, 20,  0,  0,  0, 1,2,3,4,5,6,7,8,
     5, -5,-10,  0,  0,-10, -5,  5, 1,2,3,4,5,6,7,8,
     5, 10, 10,-20,-20, 10, 10,  5, 1,2,3,4,5,6,7,8,
     0,  0,  0,  0,  0,  0,  0,  0, 1,2,3,4,5,6,7,8],

    [0,	0,	0,	0,	0,	 0,	0,	0,	1,2,3,4,5,6,7,8,
        5,	10,	10,	-20,-20,10,	10,	5,	1,2,3,4,5,6,7,8,
        5,	-5,	-10, 0,	0,  -10,-5,	5,	1,2,3,4,5,6,7,8,
        0,	0,	0,	20,	20, 0,	0,	0,	1,2,3,4,5,6,7,8,
        5,	5,	10,	25,	25,	10,	5,	5,	1,2,3,4,5,6,7,8,
        10,	10,	20,	30,	30,	20,	10,	10,	1,2,3,4,5,6,7,8,
        50,	50,	50,	50,	50,	50,	50,	50,	1,2,3,4,5,6,7,8,
        0,	0,	0,	0,	0,	0,	0,	0,  1,2,3,4,5,6,7,8],

    [-50,-40,-30,-30,-30,-30,-40,-50,    1,2,3,4,5,6,7,8,
        -40,-20,  0,  0,  0,  0,-20,-40,    1,2,3,4,5,6,7,8,
        -30,  0, 10, 15, 15, 10,  0,-30,    1,2,3,4,5,6,7,8,
        -30,  5, 15, 20, 20, 15,  5,-30,    1,2,3,4,5,6,7,8,
        -30,  0, 15, 20, 20, 15,  0,-30,    1,2,3,4,5,6,7,8,
        -30,  5, 10, 15, 15, 10,  5,-30,    1,2,3,4,5,6,7,8,
        -40,-20,  0,  5,  5,  0,-20,-40,    1,2,3,4,5,6,7,8,
        -50,-40,-30,-30,-30,-30,-40,-50,    1,2,3,4,5,6,7,8],

    [-50, -40,-30, -30,-30,-30, -40, -50,    1,2,3,4,5,6,7,8,
        -40, -20,  0,   5,  5, 0, -20,  -40,    1,2,3,4,5,6,7,8,
        -30,   5, 10,  15, 15, 10,  5,  -30,    1,2,3,4,5,6,7,8,
        -30,   0, 15,  20, 20, 15,  0,  -30,    1,2,3,4,5,6,7,8,
        -30,   5, 15,  20, 20, 15,  5,  -30,    1,2,3,4,5,6,7,8,
        -30,   0, 10,  15, 15, 10,  0,  -30,    1,2,3,4,5,6,7,8,
        -40, -20,  0,   0,  0,  0, -20, -40,    1,2,3,4,5,6,7,8,
        -50, -40,-30, -30,-30,-30, -40, -50,    1,2,3,4,5,6,7,8],

    [-20,-10,-10,-10,-10,-10,-10,-20,        1,2,3,4,5,6,7,8,
        -10,  0,  0,  0,  0,  0,  0,-10,        1,2,3,4,5,6,7,8,
        -10,  0,  5, 10, 10,  5,  0,-10,        1,2,3,4,5,6,7,8,
        -10,  5,  5, 10, 10,  5,  5,-10,        1,2,3,4,5,6,7,8,
        -10,  0, 10, 10, 10, 10,  0,-10,        1,2,3,4,5,6,7,8,
        -10, 10, 10, 10, 10, 10, 10,-10,        1,2,3,4,5,6,7,8,
        -10,  5,  0,  0,  0,  0,  5,-10,        1,2,3,4,5,6,7,8,
        -20,-10,-10,-10,-10,-10,-10,-20,        1,2,3,4,5,6,7,8],

    [-20, -10, -10, -10, -10, -10, -10,-20,    8, 7, 6, 5, 4, 3, 2, 1, 
        -10,   5,   0,   0,   0,  0,   5, -10,    8, 7, 6, 5, 4, 3, 2, 1, 
        -10,  10,  10,  10,  10, 10,  10, -10,    8, 7, 6, 5, 4, 3, 2, 1, 
        -10,   0,  10,  10,  10, 10,   0, -10,    8, 7, 6, 5, 4, 3, 2, 1, 
        -10,   5,   5,  10,  10,  5,   5, -10,    8, 7, 6, 5, 4, 3, 2, 1, 
        -10,   0,   5,  10,  10,  5,   0, -10,    8, 7, 6, 5, 4, 3, 2, 1, 
        -10,   0,   0,   0,   0,  0,   0, -10,    8, 7, 6, 5, 4, 3, 2, 1, 
        -20, -10, -10, -10, -10, -10, -10,-20,    8, 7, 6, 5, 4, 3, 2, 1],

    [0,  0,  0,  0,  0,  0,  0,  0,      1,2,3,4,5,6,7,8,
        5, 10, 10, 10, 10, 10, 10,  5,     1,2,3,4,5,6,7,8,
        -5,  0,  0,  0,  0,  0,  0, -5,     1,2,3,4,5,6,7,8,
        -5,  0,  0,  0,  0,  0,  0, -5,     1,2,3,4,5,6,7,8,
        -5,  0,  0,  0,  0,  0,  0, -5,     1,2,3,4,5,6,7,8,
        -5,  0,  0,  0,  0,  0,  0, -5,     1,2,3,4,5,6,7,8,
        -5,  0,  0,  0,  0,  0,  0, -5,     1,2,3,4,5,6,7,8,
        0,  0,  0,  5,  5,  0,  0,  0,     1,2,3,4,5,6,7,8],

    [0, 0, 0, 5, 5, 0, 0, 0,      8, 7, 6, 5, 4, 3, 2, 1,
        -5, 0, 0, 0, 0, 0, 0,-5,      8, 7, 6, 5, 4, 3, 2, 1,
        -5, 0, 0, 0, 0, 0, 0,-5,      8, 7, 6, 5, 4, 3, 2, 1,
        -5, 0, 0, 0, 0, 0, 0,-5,      8, 7, 6, 5, 4, 3, 2, 1,
        -5, 0, 0, 0, 0, 0, 0,-5,      8, 7, 6, 5, 4, 3, 2, 1,
        -5, 0, 0, 0, 0, 0, 0,-5,      8, 7, 6, 5, 4, 3, 2, 1,
        5, 10,10,10,10,10,10, 5,      8, 7, 6, 5, 4, 3, 2, 1,
        0,  0, 0, 0, 0, 0, 0, 0,      8, 7, 6, 5, 4, 3, 2, 1],

    [-20,-10,-10, -5, -5,-10,-10,-20,    1,2,3,4,5,6,7,8,
        -10,  0,  0,  0,  0,  0,  0,-10,    1,2,3,4,5,6,7,8,
        -10,  0,  5,  5,  5,  5,  0,-10,    1,2,3,4,5,6,7,8,
        -5,  0,  5,  5,  5,  5,  0, -5,    1,2,3,4,5,6,7,8,
        0,  0,  5,  5,  5,  5,  0, -5,    1,2,3,4,5,6,7,8,
        -10,  5,  5,  5,  5,  5,  0,-10,    1,2,3,4,5,6,7,8,
        -10,  0,  5,  0,  0,  0,  0,-10,    1,2,3,4,5,6,7,8,
        -20,-10,-10, -5, -5,-10,-10,-20,    1,2,3,4,5,6,7,8],

    [-20,-10,-10,-5,-5,-10,-10,-20,  8, 7, 6, 5, 4, 3, 2, 1, 
        -10, 0,  0,  0, 0, 5,  0, -10,  8, 7, 6, 5, 4, 3, 2, 1, 
        -10, 0,  5,  5, 5, 5,  5, -10,  8, 7, 6, 5, 4, 3, 2, 1, 
        -5,  0,  5,  5, 5, 5,  0,  -5,  8, 7, 6, 5, 4, 3, 2, 1, 
        -5,  0,  5,  5, 5, 5,  0,  -5,  8, 7, 6, 5, 4, 3, 2, 1, 
        -10, 0,  5,  5, 5, 5,  0, -10,  8, 7, 6, 5, 4, 3, 2, 1, 
        -10, 0,  0,  0, 0, 0,  0, -10,  8, 7, 6, 5, 4, 3, 2, 1, 
        -20,-10,-10,-5,-5,-10,-10,-20,  8, 7, 6, 5, 4, 3, 2, 1],

    [-30,-40,-40,-50,-50,-40,-40,-30,    1,2,3,4,5,6,7,8,
        -30,-40,-40,-50,-50,-40,-40,-30,    1,2,3,4,5,6,7,8,
        -30,-40,-40,-50,-50,-40,-40,-30,    1,2,3,4,5,6,7,8,
        -30,-40,-40,-50,-50,-40,-40,-30,    1,2,3,4,5,6,7,8,
        -20,-30,-30,-40,-40,-30,-30,-20,    1,2,3,4,5,6,7,8,
        -10,-20,-20,-20,-20,-20,-20,-10,    1,2,3,4,5,6,7,8,
        20, 20,  0,  0,  0,  0, 20, 20,    1,2,3,4,5,6,7,8,
        20, 30, 10,  0,  0, 10, 30, 20,    1,2,3,4,5,6,7,8],

    [-30,-40,-40,-50,-50,-40,-40,-30,    1,2,3,4,5,6,7,8,
        -30,-40,-40,-50,-50,-40,-40,-30,    1,2,3,4,5,6,7,8,
        -30,-40,-40,-50,-50,-40,-40,-30,    1,2,3,4,5,6,7,8,
        -30,-40,-40,-50,-50,-40,-40,-30,    1,2,3,4,5,6,7,8,
        -20,-30,-30,-40,-40,-30,-30,-20,    1,2,3,4,5,6,7,8,
        -10,-20,-20,-20,-20,-20,-20,-10,    1,2,3,4,5,6,7,8,
        5, 5,  10, 10, 10, 10, 5, 5,    1,2,3,4,5,6,7,8,
        -20,-10, 0,  0,  0, 0, -10,-20,    1,2,3,4,5,6,7,8],

    [20,  30,  10,   0,   0,  10,  30,  20,      8, 7, 6, 5, 4, 3, 2, 1,
        20,  20,   0,   0,   0,   0,  20,  20,      8, 7, 6, 5, 4, 3, 2, 1,
        -10, -20, -20, -20, -20, -20, -20, -10,      8, 7, 6, 5, 4, 3, 2, 1,
        -20, -30, -30, -40, -40, -30, -30, -20,      8, 7, 6, 5, 4, 3, 2, 1,
        -30, -40, -40, -50, -50, -40, -40, -30,      8, 7, 6, 5, 4, 3, 2, 1,
        -30, -40, -40, -50, -50, -40, -40, -30,      8, 7, 6, 5, 4, 3, 2, 1,
        -30, -40, -40, -50, -50, -40, -40, -30,      8, 7, 6, 5, 4, 3, 2, 1,
        -30, -40, -40, -50, -50, -40, -40, -30,      8, 7, 6, 5, 4, 3, 2, 1]])


def evaluate(board, side):
    local_board = np.array(board.board)
    return count_material(local_board, side) + consider_positions(local_board, side)


def consider_positions(board, side):
    perspective = 1 if side == white else -1

    #timer = time.time()

    val = np.sum(board_positions[board == np.arange(1, 14)[:, np.newaxis]])

    #print(time.time() - timer)

    return val*perspective

def count_material(local_board, side):
    perspective = 1 if side == white else -1

    val = np.sum(piece_values[local_board])

    return val*perspective