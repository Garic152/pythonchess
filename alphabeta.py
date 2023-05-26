import time
import copy
import evaluate
import main

from main import Moves

tree_size = 0

def minimax(allowed_time: int, depth: int, board: main.Board):
    global tree_size

    tree_size = 0
    
    #define for which side minimax should run
    maximize = board.side
    best_value = -float("inf") if maximize else float("inf")
    
    #init time for time_management
    timer = time.time()

    #start generating the first moves
    moves = Moves()
    moves.count = 0
    main.generate_move(moves, board)
    
    #if lenth is zero the game is over or something went wrong
    if len(moves.moves) == 0:
        return 0

    boardcopy = copy.deepcopy(board)
    for move in moves:
        tree_size += 1
        main.print_board(board)
        inp = input("")
        #return best move after the allowed time is passed
        if time.time() - timer > allowed_time:
            return best_move

        board.copy_move()

        if not main.make_move(move, board):
            continue

        value = alpha_beta(depth - 1, not maximize, board)
        board = copy.deepcopy(boardcopy)

        board.undo_move()

        if maximize and value >= best_value:
            best_value = value
            best_move = move
        elif not maximize and value <= best_value:
            best_value = value
            best_move = move
    print(tree_size)
    return best_move


def alpha_beta(depth: int, maximize: bool, board):
    #look if the alpha_beta function should optimize for white or black,
    #then initialize with the corresponding initial values of -inf and inf for alpha and beta
    if maximize:
        return alpha_beta_max(-float("inf"), float("inf"), depth, board)
    else:
        return alpha_beta_min(-float("inf"), float("inf"), depth, board)


def alpha_beta_max(alpha, beta, depth, board):
    global tree_size
    #check if depth is 0, if yes evaluate and return the current board
    if depth == 0:
        return evaluate.evaluate(board, board.side)

    moves = Moves()
    main.generate_move(moves, board)

    for move in moves:
        tree_size += 1
        #copy move, make it and then pass it into min
        board.copy_move()

        if not main.make_move(move, board):
            print("ILLEGAL MOVE")
            continue

        print("MAX CALLED")
        print("Depth: " + str(depth))
        main.print_board(board)
        inp = input("")

        value = alpha_beta_min(alpha, beta, depth - 1, board)

        board.undo_move()

        if value >= beta:
            return beta
        elif value > alpha:
            alpha = value
    return alpha


def alpha_beta_min(alpha, beta, depth, board):
    global tree_size
    #check if depth is 0, if yes evaluate and return the current board
    if depth == 0:
        #return evaluate(board)
        return evaluate.evaluate(board, board.side)
    
    moves = Moves()
    main.generate_move(moves, board)

    for move in moves:
        tree_size += 1
        #copy move, make it and then pass it into max
        board.copy_move()

        if not main.make_move(move, board):
            print("ILLEGAL MOVE")
            continue
        print("MIN CALLED")
        print("Depth: " + str(depth))
        main.print_board(board)
        inp = input("")

        value = alpha_beta_max(alpha, beta, depth - 1, board)
        board.undo_move()

        if value <= alpha:
            return alpha
        elif value < beta:
            beta = value
    return beta
