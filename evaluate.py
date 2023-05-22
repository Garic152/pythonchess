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
    -50, -40,-30, -30,-30,-30, -40,     1,2,3,4,5,6,7,8,
    -40, -20,  0,   5,   5, 0, -20,     1,2,3,4,5,6,7,8,
    -30,   5, 10,  15, 15, 10, 5,       1,2,3,4,5,6,7,8,
    -30,   0, 15,  20, 20, 15, 0,       1,2,3,4,5,6,7,8,
    -30,   5, 15,  20, 20, 15, 5,       1,2,3,4,5,6,7,8,
    -30,   0, 10,  15, 15, 10, 0,       1,2,3,4,5,6,7,8,
    -40, -20, 0,   0,  0,   0, -20,     1,2,3,4,5,6,7,8,
    -50, -40,-30, -30,-30,-30, -40,     1,2,3,4,5,6,7,8

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
      -20, -10, -10, -10, -10, -10, -10,    8, 7, 6, 5, 4, 3, 2, 1, 
      -10,   5,   0,   0,   0,  0,   5,     8, 7, 6, 5, 4, 3, 2, 1, 
      -10,  10,  10,  10,  10, 10,  10,     8, 7, 6, 5, 4, 3, 2, 1, 
      -10,   0,  10,  10,  10, 10,   0,     8, 7, 6, 5, 4, 3, 2, 1, 
      -10,   5,   5,  10,  10,  5,   5,     8, 7, 6, 5, 4, 3, 2, 1, 
      -10,   0,   5,  10,  10,  5,   0,     8, 7, 6, 5, 4, 3, 2, 1, 
      -10,   0,   0,   0,   0,  0,   0,     8, 7, 6, 5, 4, 3, 2, 1, 
      -20, -10, -10, -10, -10, -10, -10,    8, 7, 6, 5, 4, 3, 2, 1, 
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
     0, 0, 0, 5, 5, 0, 0,      8, 7, 6, 5, 4, 3, 2, 1,
    -5, 0, 0, 0, 0, 0, 0,      8, 7, 6, 5, 4, 3, 2, 1,
    -5, 0, 0, 0, 0, 0, 0,      8, 7, 6, 5, 4, 3, 2, 1,
    -5, 0, 0, 0, 0, 0, 0,      8, 7, 6, 5, 4, 3, 2, 1,
    -5, 0, 0, 0, 0, 0, 0,      8, 7, 6, 5, 4, 3, 2, 1,
    -5, 0, 0, 0, 0, 0, 0,      8, 7, 6, 5, 4, 3, 2, 1,
    5, 10,10,10,10,10,10,      8, 7, 6, 5, 4, 3, 2, 1,
    0,  0, 0, 0, 0, 0, 0,      8, 7, 6, 5, 4, 3, 2, 1
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
-20,-10,-10,-5,-5,-10,-10,  8, 7, 6, 5, 4, 3, 2, 1, 
-10, 0,  0,  0, 0, 5,  0,   8, 7, 6, 5, 4, 3, 2, 1, 
-10, 0,  5,  5, 5, 5,  5,   8, 7, 6, 5, 4, 3, 2, 1, 
-5,  0,  5,  5, 5, 5,  0,   8, 7, 6, 5, 4, 3, 2, 1, 
-5,  0,  5,  5, 5, 5,  0,   8, 7, 6, 5, 4, 3, 2, 1, 
-10, 0,  5,  5, 5, 5,  0,   8, 7, 6, 5, 4, 3, 2, 1, 
-10, 0,  0,  0, 0, 0,  0,   8, 7, 6, 5, 4, 3, 2, 1, 
-20,-10,-10,-5,-5,-10,-10,  8, 7, 6, 5, 4, 3, 2, 1 
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
     20,  30,  10,   0,   0,  10,  30,      8, 7, 6, 5, 4, 3, 2, 1,
     20,  20,   0,   0,   0,   0,  20,      8, 7, 6, 5, 4, 3, 2, 1,
    -10, -20, -20, -20, -20, -20, -20,      8, 7, 6, 5, 4, 3, 2, 1,
    -20, -30, -30, -40, -40, -30, -30,      8, 7, 6, 5, 4, 3, 2, 1,
    -30, -40, -40, -50, -50, -40, -40,      8, 7, 6, 5, 4, 3, 2, 1,
    -30, -40, -40, -50, -50, -40, -40,      8, 7, 6, 5, 4, 3, 2, 1,
    -30, -40, -40, -50, -50, -40, -40,      8, 7, 6, 5, 4, 3, 2, 1,
    -30, -40, -40, -50, -50, -40, -40,      8, 7, 6, 5, 4, 3, 2, 1
]


# positions value of pieces in early, mid and end game differ => there are different piece_square_tables
def get_position_value_table(letter_of_the_piece, phase_of_the_game):
    match letter_of_the_piece:
        case "P":
            # match phase_of_the_game
            return early_game_pawn_white
        case "p":
            return early_game_pawn_black
        case "N":
            return early_game_night_white
        case "n":
            return early_game_night_black
        case "B":
            return early_game_bishop_white
        case "b":
            return early_game_bishop_black
        case "R":
            return early_game_rook_white
        case "r":
            return early_game_rook_black
        case "Q":
            return early_game_queen_white
        case "q":
            return early_game_queen_black
        case "K":
            return early_game_king_white
        case "k":
            return early_game_king_black


def evaluate(board, side):
    # white_material_value = count_material(board, white)   #for testing
    # white_positional_value = consider_positions(board, white)
    # black_material_value = count_material(board, black)
    # black_positional_value = consider_positions(board, black)
    # print(f"white_material_value: {white_material_value} and white_positional_value: {white_positional_value}")
    # print(f"black_material_value: {black_material_value} and black_positional_value: {black_positional_value}")
    white_eval = count_material(board, white) + consider_positions(board, white)
    black_eval = count_material(board, black) + consider_positions(board, black)

    # evaluation is calculated for white. later it will be adjusted
    evaluation = white_eval - black_eval

    perspective = 1 if side == white else -1
    # adjusting the evaluation according to whose turn it is now
    return evaluation * perspective


def get_piece_positions_from_letter(letter, board):
    match letter:
        case "p":
            return board.pawn_position[black]
        case "P":
            return board.pawn_position[white]
        case "n":
            return board.night_position[black]
        case "N":
            return board.night_position[white]
        case "b":
            return board.bishop_position[black]
        case "B":
            return board.bishop_position[white]
        case "r":
            return board.rook_position[black]
        case "R":
            return board.rook_position[white]
        case "q":
            return board.queen_position[black]
        case "Q":
            return board.queen_position[white]
        case ".":
            print("wtf?")
            return board.queen_position[white]


# pieces[white] => "PNBRQ"  and pieces[black] => "pnbrq"
pieces = ["PNBRQ", "pnbrq"]


def consider_positions(board, side):
    positional_value = 0
    for piece in pieces[side]:
        for position in get_piece_positions_from_letter(piece, board):
            value_table = get_position_value_table(piece, "early")
            positional_value += value_table[position]
    return positional_value


def count_material(board, side):
    material_value = 0
    material_value += len(board.pawn_position[side]) * pawn_value
    material_value += len(board.night_position[side]) * night_value
    material_value += len(board.bishop_position[side]) * bishop_value
    material_value += len(board.rook_position[side]) * rook_value
    material_value += len(board.queen_position[side]) * queen_value
    return material_value
