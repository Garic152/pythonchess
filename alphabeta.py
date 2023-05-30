import time
import evaluate
import main
import copy

from main import Moves

tree_size = 0

def minimax(allowed_time: int, depth: int, board: main.Board):
    global tree_size

    tree_size = 0

    board.copy_move()

    maximize = board.side
    best_value = -float("inf") if maximize else float("inf")
    
    timer = time.time()

    moves = Moves()
    main.generate_move(moves, board)
    
    if len(moves.moves) == 0:
        return 0
    main.print_board(board)

    for move in moves:
        #if time.time() - timer > allowed_time:
        #    return moves.moves[1]    

        board_copy = copy.deepcopy(board)
        if not main.make_move(move, board):
            #print("ILLEGAL")
            continue        
        print("board in for loop after main.make_move() and before alpha betta")
        main.print_board(board)

        value = alpha_beta(depth - 1, not maximize, board)

        print("board in for loop after alpha_beta")
        main.print_board(board)
        board = copy.deepcopy(board_copy)

        if maximize and value >= best_value:
            best_value = value
            best_move = move
        elif not maximize and value <= best_value:
            best_value = value
            best_move = move
    
    print(tree_size)
    return best_move


def alpha_beta(depth: int, maximize: bool, board):
    if maximize:
        return alpha_beta_max(-float("inf"), float("inf"), depth, board)
    else:
        return alpha_beta_min(-float("inf"), float("inf"), depth, board)


def alpha_beta_max(alpha, beta, depth, board):
    global tree_size

    if depth == 0:
        tree_size += 1
        test1 = evaluate.evaluate(board, board.side)
        #print(f"test1: max: {test1}")
        return test1

    moves = Moves()
    main.generate_move(moves, board)

    for move in moves:

        board_copy = copy.deepcopy(board)

        if not main.make_move(move, board):
            continue

        value = alpha_beta_min(alpha, beta, depth - 1, board)

        board = copy.deepcopy(board_copy)

        if value >= beta:
            return beta
        elif value > alpha:
            alpha = value
    return alpha


def alpha_beta_min(alpha, beta, depth, board):
    global tree_size

    if depth == 0:
        tree_size += 1
        test2 = evaluate.evaluate(board, board.side^1)
        #print(f"test1: min: {test2}")
        return test2
    
    moves = Moves()
    main.generate_move(moves, board)

    for move in moves:

        board_copy = copy.deepcopy(board)

        if not main.make_move(move, board):
            #print("ILLEGAL MOVE")
            continue

        value = alpha_beta_max(alpha, beta, depth - 1, board)

        board = copy.deepcopy(board_copy)

        if value <= alpha:
            return alpha
        elif value < beta:
            beta = value
    return beta