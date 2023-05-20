white, black = range(2)

pawn_value = 100
night_value = 300
bishop_value = 300
rook_value = 500
queen_value = 900

def evaluate( board, side):
    white_eval = count_material(board,white)
    black_eval = count_material(board, black)

    evaluation = white_eval - black_eval

    perspective = 1 if side == white else -1
    return evaluation * perspective

def count_material(board, side):
    material_value = 0
    material_value += len(board.pawn_position[side]) * pawn_value
    material_value += len(board.night_position[side]) * night_value
    material_value += len(board.bishop_position[side]) * bishop_value
    material_value += len(board.rook_position[side]) * rook_value
    material_value += len(board.queen_position[side]) * queen_value
    return material_value