import main 

pawn_value = 100
night_value = 300
bishop_value = 300
rook_value = 500
queen_value = 900

def evaluate( board:main.Board, side):
    white_eval = count_material(board, main.white)
    black_eval = count_material(board, main.black)

    evaluation = white_eval - black_eval

    perspective = 1 if side == main.white else -1
    return evaluation * perspective
#def evalute():
#
#    return 0
#
def count_material(board:main.Board, side):
    material_value = 0
    material_value += len(board.pawn_position[side]) * pawn_value
    material_value += len(board.night_position[side]) * night_value
    material_value += len(board.bishop_position[side]) * bishop_value
    material_value += len(board.rook_position[side]) * rook_value
    material_value += len(board.queen_position[side]) * queen_value
    return material_value