import time

import evaluate
import main
from main import Moves

def minimax(allowed_time: int, depth: int, board: main.Board):
    #define for which side minimax should run
    maximize = board.side
    
    #init time for time_management
    timer = time.time()

    #start generating the first moves
    moves = Moves()
    main.generate_move(moves, board)
    
    #if lenth is zero the game is over or something went wrong
    if len(moves.moves) == 0:
        return 0

    for move in moves:
        #return best move after the allowed time is passed
        if time.time() - timer > allowed_time:
            return 0

        board.copy_move()

        if not main.make_move(move, board):
            return 0

        value = alpha_beta(depth - 1, not maximize, board)
        board.undo_move()

    return moves[0]


def alpha_beta(depth: int, maximize: bool, board):
    #look if the alpha_beta function should optimize for white or black,
    #then initialize with the corresponding initial values of -inf and inf for alpha and beta
    if maximize:
        return alpha_beta_max(-float("inf"), float("inf"), depth, board)
    else:
        return alpha_beta_min(-float("inf"), float("inf"), depth, board)


def alpha_beta_max(alpha, beta, depth, board):
    #check if depth is 0, if yes evaluate and return the current board
    if depth == 0:
        #return evaluate(board)
        pass

    moves = Moves()
    main.generate_move(moves, board)

    for move in moves:
        #copy move, make it and then pass it into min
        board.copy_move()

        if not main.make_move(move, board):
            return 0

        value = alpha_beta_min(alpha, beta, depth - 1, board)
        board.undo_move()

    if value >= beta:
        return beta
    elif value > alpha:
        alpha = value
    return alpha

def alpha_beta_min(alpha, beta, depth, board):
    pass
