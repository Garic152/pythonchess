white, black = range(2)


#source with explanation for the scores
#https://www.chessprogramming.org/Simplified_Evaluation_Function
pawn_value = 100
night_value = 320
bishop_value = 330
rook_value = 500
queen_value = 900

#was using list(reversed(array)) to reverse the array
early_game_pawn_white = [
    0,  0,  0,  0,  0,  0,  0,  0,  1,2,3,4,5,6,7,8,
    50, 50, 50, 50, 50, 50, 50, 50, 1,2,3,4,5,6,7,8,
    10, 10, 20, 30, 30, 20, 10, 10, 1,2,3,4,5,6,7,8,
     5,  5, 10, 25, 25, 10,  5,  5, 1,2,3,4,5,6,7,8,
     0,  0,  0, 20, 20,  0,  0,  0, 1,2,3,4,5,6,7,8,
     5, -5,-10,  0,  0,-10, -5,  5, 1,2,3,4,5,6,7,8,
     5, 10, 10,-20,-20, 10, 10,  5, 1,2,3,4,5,6,7,8,
     0,  0,  0,  0,  0,  0,  0,  0, 1,2,3,4,5,6,7,8
]

early_game_pawn_black = [
    0,	0,	0,	0,	0,	 0,	0,	0,	1,2,3,4,5,6,7,8,
    5,	10,	10,	-20,-20,10,	10,	5,	1,2,3,4,5,6,7,8,
    5,	-5,	-10, 0,	0,  -10,-5,	5,	1,2,3,4,5,6,7,8,
    0,	0,	0,	20,	20, 0,	0,	0,	1,2,3,4,5,6,7,8,
    5,	5,	10,	25,	25,	10,	5,	5,	1,2,3,4,5,6,7,8,
    10,	10,	20,	30,	30,	20,	10,	10,	1,2,3,4,5,6,7,8,
    50,	50,	50,	50,	50,	50,	50,	50,	1,2,3,4,5,6,7,8,
    0,	0,	0,	0,	0,	0,	0,	0,  1,2,3,4,5,6,7,8
]         

early_game_night_white = [
    -50,-40,-30,-30,-30,-30,-40,-50,    1,2,3,4,5,6,7,8,
    -40,-20,  0,  0,  0,  0,-20,-40,    1,2,3,4,5,6,7,8,
    -30,  0, 10, 15, 15, 10,  0,-30,    1,2,3,4,5,6,7,8,
    -30,  5, 15, 20, 20, 15,  5,-30,    1,2,3,4,5,6,7,8,
    -30,  0, 15, 20, 20, 15,  0,-30,    1,2,3,4,5,6,7,8,
    -30,  5, 10, 15, 15, 10,  5,-30,    1,2,3,4,5,6,7,8,
    -40,-20,  0,  5,  5,  0,-20,-40,    1,2,3,4,5,6,7,8,
    -50,-40,-30,-30,-30,-30,-40,-50,    1,2,3,4,5,6,7,8
]
early_game_night_black= [
    -50, -40,-30, -30,-30,-30, -40, -50,    1,2,3,4,5,6,7,8,
    -40, -20,  0,   5,  5, 0, -20,  -40,    1,2,3,4,5,6,7,8,
    -30,   5, 10,  15, 15, 10,  5,  -30,    1,2,3,4,5,6,7,8,
    -30,   0, 15,  20, 20, 15,  0,  -30,    1,2,3,4,5,6,7,8,
    -30,   5, 15,  20, 20, 15,  5,  -30,    1,2,3,4,5,6,7,8,
    -30,   0, 10,  15, 15, 10,  0,  -30,    1,2,3,4,5,6,7,8,
    -40, -20,  0,   0,  0,  0, -20, -40,    1,2,3,4,5,6,7,8,
    -50, -40,-30, -30,-30,-30, -40, -50,    1,2,3,4,5,6,7,8

]
early_game_bishop_white = [
    -20,-10,-10,-10,-10,-10,-10,-20,        1,2,3,4,5,6,7,8,
    -10,  0,  0,  0,  0,  0,  0,-10,        1,2,3,4,5,6,7,8,
    -10,  0,  5, 10, 10,  5,  0,-10,        1,2,3,4,5,6,7,8,
    -10,  5,  5, 10, 10,  5,  5,-10,        1,2,3,4,5,6,7,8,
    -10,  0, 10, 10, 10, 10,  0,-10,        1,2,3,4,5,6,7,8,
    -10, 10, 10, 10, 10, 10, 10,-10,        1,2,3,4,5,6,7,8,
    -10,  5,  0,  0,  0,  0,  5,-10,        1,2,3,4,5,6,7,8,
    -20,-10,-10,-10,-10,-10,-10,-20,        1,2,3,4,5,6,7,8
]
early_game_bishop_black = [
      -20, -10, -10, -10, -10, -10, -10,-20,    8, 7, 6, 5, 4, 3, 2, 1, 
      -10,   5,   0,   0,   0,  0,   5, -10,    8, 7, 6, 5, 4, 3, 2, 1, 
      -10,  10,  10,  10,  10, 10,  10, -10,    8, 7, 6, 5, 4, 3, 2, 1, 
      -10,   0,  10,  10,  10, 10,   0, -10,    8, 7, 6, 5, 4, 3, 2, 1, 
      -10,   5,   5,  10,  10,  5,   5, -10,    8, 7, 6, 5, 4, 3, 2, 1, 
      -10,   0,   5,  10,  10,  5,   0, -10,    8, 7, 6, 5, 4, 3, 2, 1, 
      -10,   0,   0,   0,   0,  0,   0, -10,    8, 7, 6, 5, 4, 3, 2, 1, 
      -20, -10, -10, -10, -10, -10, -10,-20,    8, 7, 6, 5, 4, 3, 2, 1, 
]

early_game_rook_white = [
    0,  0,  0,  0,  0,  0,  0,  0,      1,2,3,4,5,6,7,8,
     5, 10, 10, 10, 10, 10, 10,  5,     1,2,3,4,5,6,7,8,
    -5,  0,  0,  0,  0,  0,  0, -5,     1,2,3,4,5,6,7,8,
    -5,  0,  0,  0,  0,  0,  0, -5,     1,2,3,4,5,6,7,8,
    -5,  0,  0,  0,  0,  0,  0, -5,     1,2,3,4,5,6,7,8,
    -5,  0,  0,  0,  0,  0,  0, -5,     1,2,3,4,5,6,7,8,
    -5,  0,  0,  0,  0,  0,  0, -5,     1,2,3,4,5,6,7,8,
     0,  0,  0,  5,  5,  0,  0,  0,     1,2,3,4,5,6,7,8
]

early_game_rook_black = [
     0, 0, 0, 5, 5, 0, 0, 0,      8, 7, 6, 5, 4, 3, 2, 1,
    -5, 0, 0, 0, 0, 0, 0,-5,      8, 7, 6, 5, 4, 3, 2, 1,
    -5, 0, 0, 0, 0, 0, 0,-5,      8, 7, 6, 5, 4, 3, 2, 1,
    -5, 0, 0, 0, 0, 0, 0,-5,      8, 7, 6, 5, 4, 3, 2, 1,
    -5, 0, 0, 0, 0, 0, 0,-5,      8, 7, 6, 5, 4, 3, 2, 1,
    -5, 0, 0, 0, 0, 0, 0,-5,      8, 7, 6, 5, 4, 3, 2, 1,
    5, 10,10,10,10,10,10, 5,      8, 7, 6, 5, 4, 3, 2, 1,
    0,  0, 0, 0, 0, 0, 0, 0,      8, 7, 6, 5, 4, 3, 2, 1
]

early_game_queen_white =[
    -20,-10,-10, -5, -5,-10,-10,-20,    1,2,3,4,5,6,7,8,
    -10,  0,  0,  0,  0,  0,  0,-10,    1,2,3,4,5,6,7,8,
    -10,  0,  5,  5,  5,  5,  0,-10,    1,2,3,4,5,6,7,8,
     -5,  0,  5,  5,  5,  5,  0, -5,    1,2,3,4,5,6,7,8,
      0,  0,  5,  5,  5,  5,  0, -5,    1,2,3,4,5,6,7,8,
    -10,  5,  5,  5,  5,  5,  0,-10,    1,2,3,4,5,6,7,8,
    -10,  0,  5,  0,  0,  0,  0,-10,    1,2,3,4,5,6,7,8,
    -20,-10,-10, -5, -5,-10,-10,-20,    1,2,3,4,5,6,7,8
]

early_game_queen_black = [
-20,-10,-10,-5,-5,-10,-10,-20,  8, 7, 6, 5, 4, 3, 2, 1, 
-10, 0,  0,  0, 0, 5,  0, -10,  8, 7, 6, 5, 4, 3, 2, 1, 
-10, 0,  5,  5, 5, 5,  5, -10,  8, 7, 6, 5, 4, 3, 2, 1, 
-5,  0,  5,  5, 5, 5,  0,  -5,  8, 7, 6, 5, 4, 3, 2, 1, 
-5,  0,  5,  5, 5, 5,  0,  -5,  8, 7, 6, 5, 4, 3, 2, 1, 
-10, 0,  5,  5, 5, 5,  0, -10,  8, 7, 6, 5, 4, 3, 2, 1, 
-10, 0,  0,  0, 0, 0,  0, -10,  8, 7, 6, 5, 4, 3, 2, 1, 
-20,-10,-10,-5,-5,-10,-10,-20,  8, 7, 6, 5, 4, 3, 2, 1 
]

early_game_king_white = [
    -30,-40,-40,-50,-50,-40,-40,-30,    1,2,3,4,5,6,7,8,
    -30,-40,-40,-50,-50,-40,-40,-30,    1,2,3,4,5,6,7,8,
    -30,-40,-40,-50,-50,-40,-40,-30,    1,2,3,4,5,6,7,8,
    -30,-40,-40,-50,-50,-40,-40,-30,    1,2,3,4,5,6,7,8,
    -20,-30,-30,-40,-40,-30,-30,-20,    1,2,3,4,5,6,7,8,
    -10,-20,-20,-20,-20,-20,-20,-10,    1,2,3,4,5,6,7,8,
     20, 20,  0,  0,  0,  0, 20, 20,    1,2,3,4,5,6,7,8,
     20, 30, 10,  0,  0, 10, 30, 20,    1,2,3,4,5,6,7,8
]

early_game_king_black = [
     20,  30,  10,   0,   0,  10,  30,  20,      8, 7, 6, 5, 4, 3, 2, 1,
     20,  20,   0,   0,   0,   0,  20,  20,      8, 7, 6, 5, 4, 3, 2, 1,
    -10, -20, -20, -20, -20, -20, -20, -10,      8, 7, 6, 5, 4, 3, 2, 1,
    -20, -30, -30, -40, -40, -30, -30, -20,      8, 7, 6, 5, 4, 3, 2, 1,
    -30, -40, -40, -50, -50, -40, -40, -30,      8, 7, 6, 5, 4, 3, 2, 1,
    -30, -40, -40, -50, -50, -40, -40, -30,      8, 7, 6, 5, 4, 3, 2, 1,
    -30, -40, -40, -50, -50, -40, -40, -30,      8, 7, 6, 5, 4, 3, 2, 1,
    -30, -40, -40, -50, -50, -40, -40, -30,      8, 7, 6, 5, 4, 3, 2, 1
]


def evaluate(board, side):
    return count_material(board, side) + consider_positions(board,side)


e, P, N, B, R, Q, K, p, n, b, r, q, k, o = range(14)
# 0,1,2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13
early_game_tables = [0, #e is not a piece => no table for e
                     early_game_pawn_white,
                     early_game_night_white,
                     early_game_bishop_white,
                     early_game_rook_white,
                     early_game_queen_white,
                     early_game_king_white,
                     early_game_pawn_black,
                     early_game_night_black,
                     early_game_bishop_black,
                     early_game_rook_black,
                     early_game_queen_black,
                     early_game_king_black,
                     0] #o is not a piece => no table for o

def consider_positions(board, side):
    val_pos = 0
    perspective = 1 if side == white else -1
    for position in range(len(board.board)):
        if board.board[position] == P:

            val_pos+= early_game_tables[P][position]

        elif board.board[position] == p:

            val_pos-=early_game_tables[p][position]

        elif board.board[position] == N:

            val_pos+=early_game_tables[N][position]

        elif board.board[position] == n:

            val_pos-=early_game_tables[n][position]

        elif board.board[position] == B:

            val_pos+=early_game_tables[B][position]

        elif board.board[position] == b:

            val_pos-=early_game_tables[b][position]

        elif board.board[position] == R:

            val_pos+=early_game_tables[R][position]

        elif board.board[position] == r:

            val_pos-=early_game_tables[r][position]

        elif board.board[position] == Q:

            val_pos+=early_game_tables[Q][position]

        elif board.board[position] == q:

            val_pos-=early_game_tables[q][position]

        elif board.board[position] == K:

            val_pos+=early_game_tables[K][position]

        elif board.board[position] == k:

            val_pos-=early_game_tables[k][position]

    return val_pos*perspective

#                  e,   P,            N,            B,          R,          Q,          K, \n p, n, b, r, q, k, o = range(14)
material_values = [0, pawn_value, night_value, bishop_value, rook_value, queen_value, 20000, 
                     -pawn_value, -night_value, -bishop_value, -rook_value, -queen_value, -20000, 0,0,0] # we get sometimes figure on position 127 with value 15 that is why we have two extra zeros in the end

def  count_material(board, side):
    val = 0
    perspective = 1 if side == white else -1
    for position in range(len(board.board)):
        val += material_values[board.board[position]]
    return val*perspective