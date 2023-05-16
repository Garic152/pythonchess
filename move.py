import evaluate

def minimax(allowed_time: int, side: int, board, depth: int, alpha: int, beta: int):
    #define for which side minimax should run
    maximize = side
    
    #init time for time_management
    timer = time.time()

    #start generating the first moves
    moves = Moves()
    
    #if lenth is zero the game is over or something went wrong
    if len(moves) == 0:
        return 0

    for move in moves:
        #return best move after the allowed time is passed
        if time.time() - timer > allowed_time:
            return best_move
        
        make_move(move)



