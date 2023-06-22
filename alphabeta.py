import time
import evaluate_np as evaluate
import main
import pickle

from main import Moves
from evaluate_np import sort_moves

tree_size = 0

def sort(board: main.Board, moves: list):
    def sorter(move):
        return sort_moves(board, move)
    
    move_list = sorted(moves, key=sorter, reverse=(board.side == 0))
    return move_list


def minimax(allowed_time: int, depth: int, board: main.Board, remi_list):
    global tree_size

    tree_size = 0
    reservemove = 0
    global startdepth
    startdepth = depth-1
    maximize = board.side ^ 1
    best_value = -float("inf") if maximize else float("inf")
    best_move = 0
    timer = time.time()

    moves = Moves()
    main.generate_move(moves, board)

    if len(moves.moves) == 0:
        return 0

    for move in moves:
        remi = False
        board_copy = pickle.dumps(board)
        remicheck_copy = remi_list

        if not main.make_move(move, board):
            board = pickle.loads(board_copy)
            continue

        remicheck_copy.append(board.board)
        for pastboard in remicheck_copy:
            if remicheck_copy.count(pastboard) >= 3:
                print("Found Remi for Board:")
                main.print_board(board)
                remi = True
                move = reservemove
                break
        if remi:
            board = pickle.loads(board_copy)
            continue

        value = alpha_beta(depth - 1, not maximize, board)

        #main.print_board(board)

        board = pickle.loads(board_copy)

        if maximize and value >= best_value:
            best_value = value
            best_move = move
        elif not maximize and value <= best_value:
            best_value = value
            best_move = move

    timef = str(time.time() - timer)

    print(timef + "s")
    print("Tree size" + str(tree_size))
    print("Per second: " + str(tree_size / float(timef)))
    if not best_move:
        best_move = reservemove
    return best_move


def alpha_beta(depth: int, maximize: bool, board):
    if maximize:
        return alpha_beta_max(-float("inf"), float("inf"), depth, board, False)
    else:
        return alpha_beta_min(-float("inf"), float("inf"), depth, board, False)


def alpha_beta_max(alpha, beta, depth, board, nullmove):
    global tree_size

    if depth == 0:
        tree_size += 1
        return evaluate.evaluate(board, board.side)

    moves = Moves()
    main.generate_move(moves, board)

    #moves = sort(board, moves.moves)

    # Perform null move and evaluate the resulting position
    if depth != startdepth and depth >= 1 and not nullmove:
        null_value = alpha_beta_min(alpha, beta, depth - 1, board, True)
        if null_value >= beta:
            return beta

    for move in moves:
        board_copy = pickle.dumps(board)

        if not main.make_move(move, board):
            board = pickle.loads(board_copy)
            continue

        value = alpha_beta_min(alpha, beta, depth - 1, board, nullmove)

        board = pickle.loads(board_copy)

        if value >= beta:
            return beta
        elif value > alpha:
            alpha = value
    return alpha


def alpha_beta_min(alpha, beta, depth, board, nullmove):
    global tree_size

    if depth == 0:
        tree_size += 1
        return evaluate.evaluate(board, board.side ^ 1)

    moves = Moves()
    main.generate_move(moves, board)

    #moves = sort(board, moves.moves)

    # Perform null move and evaluate the resulting position
    if depth != startdepth and depth >= 1 and not nullmove:
        null_value = alpha_beta_max(alpha, beta, depth - 1, board, True)
        if null_value <= alpha:
            return alpha

    for move in moves:
        board_copy = pickle.dumps(board)

        if not main.make_move(move, board):
            board = pickle.loads(board_copy)
            continue

        value = alpha_beta_max(alpha, beta, depth - 1, board, nullmove)

        board = pickle.loads(board_copy)

        if value <= alpha:
            return alpha
        elif value < beta:
            beta = value
    return beta