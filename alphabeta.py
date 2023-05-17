import time

import evaluate
import main_copy as main

def minimax(allowed_time: int, depth: int, board: main.Board):
    #define for which side minimax should run
    maximize = board.side
    
    #init time for time_management
    timer = time.time()

    #start generating the first moves
    moves = main.Moves()
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
    pass
