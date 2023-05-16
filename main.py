"""
Trying out some chess engine stuff
"""

from random import randrange
import time
from timeit import default_timer as timer

import evaluate

#defining the piece integer representation
e, P, N, B, R, Q, K, p, n, b, r, q, k, o = range(14)

white, black = range(2)

Castling = {'KC': 1, 'QC': 2, 'kc': 4, 'qc': 8}

board = [
    r, n, b, q, k, b, n, r, o, o, o, o, o, o, o, o,
    p, p, p, p, p, p, p, p, o, o, o, o, o, o, o, o,
    e, e, e, e, e, e, e, e, o, o, o, o, o, o, o, o,
    e, e, e, e, e, e, e, e, o, o, o, o, o, o, o, o,
    e, e, e, e, e, e, e, e, o, o, o, o, o, o, o, o,
    e, e, e, e, e, e, e, e, o, o, o, o, o, o, o, o,
    P, P, P, P, P, P, P, P, o, o, o, o, o, o, o, o,
    R, N, B, Q, K, B, N, R, o, o, o, o, o, o, o, o
]

square_representation = [
    'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8', 'i8', 'j8', 'k8', 'l8', 'm8', 'n8', 'o8', 'p8',
    'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7', 'i7', 'j7', 'k7', 'l7', 'm7', 'n7', 'o7', 'p7',
    'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6', 'i6', 'j6', 'k6', 'l6', 'm6', 'n6', 'o6', 'p6',
    'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5', 'i5', 'j5', 'k5', 'l5', 'm5', 'n5', 'o5', 'p5',
    'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4', 'i4', 'j4', 'k4', 'l4', 'm4', 'n4', 'o4', 'p4',
    'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3', 'i3', 'j3', 'k3', 'l3', 'm3', 'n3', 'o3', 'p3',
    'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2', 'i2', 'j2', 'k2', 'l2', 'm2', 'n2', 'o2', 'p2',
    'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1', 'i1', 'j1', 'k1', 'l1', 'm1', 'n1', 'o1', 'p1'
]


char_ascii = '.PNBRQKpnbrqk'
char_sides = 'wb'
countercheck = 0

#from ascii to normal chars
char_pieces = {'P': P, 'N': N, 'B': B, 'R': R, 'Q': Q, 'K': K, 'p': p, 'n': n, 'b': b, 'r': r, 'q': q, 'k': k}
promoted_pieces = {Q: 'q', R: 'r', B: 'b', N: 'n', q: 'q', r: 'r', b: 'b', n: 'n'}


start_position = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
fen = 'r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1'


#0 = white and 1 = black
side = white

#castling rights in bit representation, where 15 is 1111, meaning both sides can castle both on the queen and king side
can_castle = 0

#castling rights
castling_rights = [
    7, 15, 15, 15,  3, 15, 15, 11,  o, o, o, o, o, o, o, o,
    15, 15, 15, 15, 15, 15, 15, 15,  o, o, o, o, o, o, o, o,
    15, 15, 15, 15, 15, 15, 15, 15,  o, o, o, o, o, o, o, o,
    15, 15, 15, 15, 15, 15, 15, 15,  o, o, o, o, o, o, o, o,
    15, 15, 15, 15, 15, 15, 15, 15,  o, o, o, o, o, o, o, o,
    15, 15, 15, 15, 15, 15, 15, 15,  o, o, o, o, o, o, o, o,
    15, 15, 15, 15, 15, 15, 15, 15,  o, o, o, o, o, o, o, o,
    13, 15, 15, 15, 12, 15, 15, 14,  o, o, o, o, o, o, o, o
    ]

#king position
king_position = [116, 4]

#piece movement offsets
knight_movement = [33, 31, 18, 14, -33, -31, -18, -14]
bishop_movement = [15, 17, -15, -17]
rook_movement = [16, -16, 1, -1]
king_movement = [16, -16, 1, -1, 15, 17, -15, -17]

""" /*
    Move formatting
    
    0000 0000 0000 0000 0111 1111       current position
    0000 0000 0011 1111 1000 0000       target position
    0000 0011 1100 0000 0000 0000       promotion piece
    0000 0100 0000 0000 0000 0000       captures
    0000 1000 0000 0000 0000 0000       double pawn move
    0001 0000 0000 0000 0000 0000       castling

*/ """


# define movement information with bits
def set_move(current, target, promotion_piece, capture, double_pawn, castling):
    return (
        current
        | (target << 7)
        | (promotion_piece << 14)
        | (capture << 18)
        | (double_pawn << 19)
        | (castling << 20)
    )


# extract the information
def get_move_source(move):
    return move & 0x7F


def get_move_target(move):
    return (move >> 7) & 0x7F


def get_move_piece(move):
    return (move >> 14) & 0xF


def get_move_capture(move):
    return (move >> 18) & 0x1


def get_move_pawn(move):
    return (move >> 19) & 0x1


def get_move_castling(move):
    return (move >> 20) & 0x1


#move list
class Moves:
    def __init__(self):
        self.moves = []
        self.count = 0

    
    def add_move(self, move):
        #add move to the list
        self.moves.append(move)

        #increase move counter
        self.count += 1


    def __getitem__(self, index):
        return self.moves[index]


def clear_board():
    # loop over column
    for rank in range(8):
        # loop over row
        for file in range(16):
            position = file + rank * 16
            # check if the piece is on the field
            if not position & 0x88:
                # clears the board
                board[position] = e


def print_board():
    # loop over column
    for rank in range(8):
        # loop over row
        for file in range(16):
            if file == 0:
                print(8 - rank, end="   ")
            position = file + rank * 16
            # check if the piece is on the field
            if not position & 0x88:
                print(char_ascii[board[position]], end=" ")
        print(end="\n")
    print("\n    A B C D E F G H")


def is_position_attacked(position, side):
    # attacked by pawn
    if not side:
        if not ((position + 17) & 0x88) and board[position + 17] == P:
            return True
        elif not ((position + 15) & 0x88) and board[position + 15] == P:
            return True
    else:
        if not ((position - 17) & 0x88) and board[position - 17] == p:
            return True
        elif not ((position - 15) & 0x88) and board[position - 15] == p:
            return True

    # attacked by knight
    if not side:
        for move in knight_movement:
            if not ((position + move) & 0x88) and board[position + move] == N:
                return True
    else:
        for move in knight_movement:
            if not ((position + move) & 0x88) and board[position + move] == n:
                return True

    # attacked by king
    if not side:
        for move in king_movement:
            if not ((position + move) & 0x88) and board[position + move] == K:
                return True
    else:
        for move in king_movement:
            if not ((position + move) & 0x88) and board[position + move] == k:
                return True


    # attacked by Bishop and Queen
    for move in bishop_movement:
        # creates new temp position
        new_position = position + move

        # loop through all the available positions for one move
        while not ((new_position) & 0x88):
            # grabs the piece at current position

            target = board[new_position]

            # checks if the position is attacked by B & Q
            if (
                (target == B or target == Q)
                if not side
                else (target == b or target == q)
            ):
                return True

            # breaks if it hits a piece
            elif target != 0:
                break

            # increment to new next position
            new_position += move

    # attacked by Rook and Queen
    for move in rook_movement:
        new_position = position + move

        while not ((new_position) & 0x88):
            target = board[new_position]

            if (
                (target == R or target == Q)
                if not side
                else (target == r or target == q)
            ):
                return True

            elif target != 0:
                break

            new_position += move
    return 0

def print_attack():
    # loop over column
    for rank in range(8):
        # loop over row
        for file in range(16):
            if file == 0:
                print(rank + 1, end="   ")
            position = file + rank * 16
            # check if the piece is on the field
            if not position & 0x88:
                print("x" if is_position_attacked(position, side) else ".", end=" ")
        print(end="\n")
    print("\n    A B C D E F G H")


def print_stats():
    global can_castle_str
    print("Side to move: " + char_sides[side])
    print("Castling: " + str(bin(can_castle)[2:]).rjust(4, "0"))


def load_fen(fen):
    global side
    global can_castle
    fen_position = 0

    # reset board
    clear_board()

    # loop over column
    for rank in range(8):
        # loop over row
        file = 0
        while file <= 16:
            # calculate current position
            position = file + rank * 16
            # check if the piece is on the field
            if not position & 0x88:
                if (fen[fen_position] > "a" and fen[fen_position] < "z") or (
                    fen[fen_position] > "A" and fen[fen_position] < "Z"):

                    #set king square
                    if (fen[fen_position] == 'K'):
                        king_position[white] = position
                
                    elif (fen[fen_position] == 'k'):
                        king_position[black] = position


                    # set current board position to fen piece
                    board[position] = char_pieces[fen[fen_position]]

                    fen_position += 1

                elif fen[fen_position] > "0" and fen[fen_position] < "9":
                    file += int(fen[fen_position]) - 1

                    fen_position += 1

                elif fen[fen_position] == "/" or fen[fen_position] == " ":
                    fen_position += 1
            file += 1

    # go to side position
    fen_position += 1

    # parse side to move
    side = white if fen[fen_position] == "w" else black

    # go to castling position
    fen_position += 2

    while fen[fen_position] != " ":
        if fen[fen_position] == "K":
            can_castle |= Castling["KC"]
        elif fen[fen_position] == "Q":
            can_castle |= Castling["QC"]
        elif fen[fen_position] == "k":
            can_castle |= Castling["kc"]
        elif fen[fen_position] == "q":
            can_castle |= Castling["qc"]
        elif fen[fen_position] == "-":
            break
        fen_position += 1


# move generation
def generate_move(move):
    # loop over all positions on the board
    for position in range(128):
        if not position & 0x88:
            # white moves
            if not side:
                # pawn moves + captures
                if board[position] == P:
                    # move forward
                    if not (position - 16) & 0x88 and not board[position - 16]:
                        # promotion condition
                        if position > 15 and position < 24:
                            move.add_move(set_move(position, position - 16, Q, 0, 0, 0))
                            move.add_move(set_move(position, position - 16, R, 0, 0, 0))
                            move.add_move(set_move(position, position - 16, B, 0, 0, 0))
                            move.add_move(set_move(position, position - 16, N, 0, 0, 0))

                        # other pawn moves
                        else:
                            # move one square ahead
                            move.add_move(set_move(position, position - 16, 0, 0, 0, 0))

                            # move to squares
                            if (position > 95 and position < 104) and not board[
                                position - 32
                            ]:
                                #move 2 squares ahead
                                move.add_move(set_move(position, position - 32, 0, 0, 1, 0))

                    # pawn capture moves
                    for movement in bishop_movement:
                        if (
                            not (position - movement) & 0x88
                            and board[position - movement]
                            and movement > 0
                            and board[position - movement] > 6
                        ):
                            # look for promotion capture
                            if position > 15 and position < 24:
                                pass
                                move.add_move(set_move(position, position - movement, Q, 1, 0, 0))
                                move.add_move(set_move(position, position - movement, R, 1, 0, 0))
                                move.add_move(set_move(position, position - movement, B, 1, 0, 0))
                                move.add_move(set_move(position, position - movement, N, 1, 0, 0))

                            # casual capture
                            else:
                                pass
                                move.add_move(set_move(position, position - movement, 0, 1, 0, 0))

                # white king castling
                if board[position] == K:
                    # check king side castle
                    if (
                        can_castle & Castling["KC"]
                        and position == 116
                        and not board[117]
                        and not board[118]
                        and board[119] == R
                    ):
                        # temp variable to check if any pieces king side are attacked
                        is_attacked = False
                        for i in range(116, 119):
                            if is_position_attacked(i, black):
                                is_attacked = True

                        if not is_attacked:
                            pass
                            move.add_move(set_move(116, 118, 0, 0, 0, 1))

                    # check queen side castle
                    if (
                        can_castle & Castling["QC"]
                        and position == 116
                        and not board[115]
                        and not board[114]
                        and not board[113]
                        and board[112] == R
                    ):
                        # temp variable to check if any pieces king side are attacked
                        is_attacked = False
                        for i in range(113, 117):
                            if is_position_attacked(i, black):
                                is_attacked = True

                        if not is_attacked:
                            pass
                            move.add_move(set_move(116, 114, 0, 0, 0, 1))

            # black moves
            else:
                # pawn moves + captures
                if board[position] == p:
                    if not (position + 16) & 0x88 and not board[position + 16]:
                        if position > 95 and position < 104:
                            pass
                            move.add_move(set_move(position, position + 16, q, 0, 0, 0))
                            move.add_move(set_move(position, position + 16, r, 0, 0, 0))
                            move.add_move(set_move(position, position + 16, b, 0, 0, 0))
                            move.add_move(set_move(position, position + 16, n, 0, 0, 0))

                        else:
                            pass
                            move.add_move(set_move(position, position + 16, 0, 0, 0, 0))

                            if (position > 15 and position < 24) and not board[
                                position + 32
                            ]:
                                pass
                                move.add_move(set_move(position, position + 32, 0, 0, 1, 0))

                    for movement in bishop_movement:
                        if (
                            not (position - movement) & 0x88
                            and board[position - movement]
                            and movement < 0
                            and board[position - movement] < 7
                        ):
                            if position > 95 and position < 104:
                                pass
                                move.add_move(set_move(position, position + movement, q, 1, 0, 0))
                                move.add_move(set_move(position, position + movement, r, 1, 0, 0))
                                move.add_move(set_move(position, position + movement, b, 1, 0, 0))
                                move.add_move(set_move(position, position + movement, n, 1, 0, 0))

                            else:
                                pass
                                move.add_move(set_move(position, position + movement, 0, 1, 0, 0))

                # black king castling, doucmentation in white king moves
                if board[position] == k:
                    if (
                        can_castle & Castling["kc"]
                        and position == 4
                        and not board[5]
                        and not board[6]
                        and board[7] == r
                    ):
                        is_attacked = False
                        for i in range(4, 7):
                            if is_position_attacked(i, white):
                                is_attacked = True

                        if not is_attacked:
                            pass
                            move.add_move(set_move(4, 6, 0, 0, 0, 1))

                    if (
                        can_castle & Castling["qc"]
                        and position == 4
                        and not board[3]
                        and not board[2]
                        and not board[1]
                        and board[0] == r
                    ):
                        is_attacked = False
                        for i in range(1, 5):
                            if is_position_attacked(i, white):
                                is_attacked = True

                        if not is_attacked:
                            pass
                            move.add_move(set_move(4, 2, 0, 0, 0, 1))

            # knight moves and captures
            if (board[position] == N) if not side else (board[position] == n):
                # loop over knight moves
                for movement in knight_movement:
                    # check if targeted square is on board
                    if not (position + movement) & 0x88:
                        # safe target piece for capture checks
                        target = board[position + movement]

                        # 2 situations for either white or black pieces
                        if (
                            (not target or (target >= 7 and target <= 12))
                            if not side
                            else (not target or (target >= 1 and target <= 6))
                        ):
                            # check if it captured something or hits empty square
                            if target:
                                pass
                                move.add_move(set_move(position, position + movement, 0, 1, 0, 0))

                            else:
                                pass
                                move.add_move(set_move(position, position + movement, 0, 0, 0, 0))

            # king standart moves and captures comments same as in knight moves
            if (board[position] == K) if not side else (board[position] == k):
                for movement in king_movement:
                    if not (position + movement) & 0x88:
                        target = board[position + movement]

                        if (
                            (not target or (target >= 7 and target <= 12))
                            if not side
                            else (not target or (target >= 1 and target <= 6))
                        ):
                            if target:
                                pass
                                move.add_move(set_move(position, position + movement, 0, 1, 0, 0))

                            else:
                                pass
                                move.add_move(set_move(position, position + movement, 0, 0, 0, 0))

            # bishop and queen movement
            if (
                ((board[position] == B) or (board[position] == Q))
                if not side
                else ((board[position] == b) or (board[position] == q))
            ):
                # loop over bishop and queen moves
                for movement in bishop_movement:
                    # safe target square and increment
                    target = position + movement

                    current_movement = movement
                    while not target & 0x88:
                        # get piece at targeted position
                        piece = board[target]

                        # if it hits own piece
                        if (
                            (piece >= 1 and piece <= 6)
                            if not side
                            else (piece >= 7 and piece <= 12)
                        ):
                            break

                        # if it hits opponent piece
                        if (
                            (piece >= 7 and piece <= 12)
                            if not side
                            else (piece >= 1 and piece <= 6)
                        ):
                            move.add_move(set_move(position, position + current_movement, 0, 1, 0, 0))
                            break

                        # if square empty
                        if not piece:
                            move.add_move(set_move(position, position + current_movement, 0, 0, 0, 0))
                            pass

                        current_movement += movement
                        target += movement

            # rook and queen movement documentation in above code
            if (
                ((board[position] == R) or (board[position] == Q))
                if not side
                else ((board[position] == r) or (board[position] == q))
            ):
                for movement in rook_movement:
                    target = position + movement
                    current_movement = movement

                    while not target & 0x88:
                        piece = board[target]

                        if (
                            (piece >= 1 and piece <= 6)
                            if not side
                            else (piece >= 7 and piece <= 12)
                        ):
                            break

                        if (
                            (piece >= 7 and piece <= 12)
                            if not side
                            else (piece >= 1 and piece <= 6)
                        ):
                            move.add_move(set_move(position, position + current_movement, 0, 1, 0, 0))
                            break

                        # if square empty
                        if not piece:
                            move.add_move(set_move(position, position + current_movement, 0, 0, 0, 0))
                            pass
                        
                        current_movement += movement
                        target += movement

#make move
def make_move(move):
    global side
    global board
    global king_position
    global can_castle
    global countercheck


    #define board state copy variable
    board_copy = [0] * 128
    king_position_copy = [2]
    side_copy = 0
    can_castle_copy = 0


    #copy board state
    board_copy = board.copy()
    king_position_copy = king_position.copy()
    side_copy = side
    can_castle_copy = can_castle

    #get current and target position
    position = get_move_source(move)
    target = get_move_target(move)
    promoted_piece = get_move_piece(move)
    castling = get_move_castling(move)

    #print("Moving " + square_representation[position] + " to " + square_representation[target])

    #if target is king
    if board[target] == K or board[target] == k:
        return 0

    #make the move
    board[target] = board[position]
    board[position] = e

    #promote pawn
    if promoted_piece:
        board[target] = promoted_piece

    #update king position
    if board[position] == K or board[position] == k:
        king_position[side] = target

    #castling moves
    if castling:
        match target:
            case 118:
                board[117] = board[119]
                board[119] = e
            case 6:
                board[5] = board[7]
                board[7] = e
            case 114:
                board[115] = board[112]
                board[112] = e
            case 2:
                board[3] = board[0]
                board[0] = e

    #change castling rights
    can_castle &= castling_rights[position]
    can_castle &= castling_rights[target]

    #change side
    side ^= 1

    #print("Moving " + square_representation[position] + " to " + square_representation[target])

    #is king attacked
    if is_position_attacked(king_position[side^1], side):
        
        #illegal move
        #restore board
        board = board_copy
        king_position = king_position_copy
        side = side_copy
        can_castle = can_castle_copy
        return 0

    else:
        #legal move

        return 1


#define tree length
tree_size = 0

def get_time_ms():
    return time.process_time() 

def chess(depth):
    global tree_size
    #break when depth = 0
    if not depth:
        tree_size += 1
        return

    global side
    global board
    global king_position
    global can_castle

    #generate move
    moves = Moves()
    moves.count = 0
    generate_move(moves)

    for move in moves:
        #define board state copy variable
        board_copy = [0] * 128
        king_position_copy = [2]
        side_copy = 0
        can_castle_copy = 0
        
        #copy board state
        board_copy = board.copy()
        king_position_copy = king_position.copy()
        side_copy = side
        can_castle_copy = can_castle

        #only legal moves
        if not make_move(move):
            continue

        #recursive until depth = 0
        chess(depth - 1)
        
        #restore board
        board = board_copy
        king_position = king_position_copy
        side = side_copy
        can_castle = can_castle_copy

    
def chess_perft(depth):
    #initializing access to global variables
    global tree_size
    global side
    global board
    global king_position
    global can_castle
    global attack_count

    #generate move
    moves = Moves()
    #moves.count = 0
    generate_move(moves)

    for move in moves:
        #define board state copy variable
        board_copy = [0] * 128
        king_position_copy = [2]
        side_copy = 0
        can_castle_copy = 0

        #copy board state
        board_copy = board.copy()
        king_position_copy = king_position.copy()
        side_copy = side
        can_castle_copy = can_castle

        #only legal moves
        if not make_move(move):
            continue

        #recursive until depth = 0
        chess(depth - 1)

        #restore board
        board = board_copy
        king_position = king_position_copy
        side = side_copy
        can_castle = can_castle_copy

    return moves[randrange(0, moves.count)]


def check_mate():
    global tree_size
    global side
    global board
    global king_position
    global can_castle
    
    moves = Moves()
    # moves.count = 0
    generate_move(moves)
    checklist = []
    for move in moves:
        # copy board state
        board_copy = board.copy()
        king_position_copy = king_position.copy()
        side_copy = side
        can_castle_copy = can_castle

        if not make_move(move):
            continue
        checklist.append(move)
        # restore board
        board = board_copy
        king_position = king_position_copy
        side = side_copy
        can_castle = can_castle_copy
    return checklist == []

#loop over game
def loop_game(depth):
    checkmate = False
    remi = False
    boards = []
    while not checkmate:

        #get and make best move
        best_move = chess_perft(depth)
        make_move(best_move)

        #print best move and board
        print("Best move: " + char_ascii[board[get_move_target(best_move)]] + " on "  + square_representation[get_move_source(best_move)] + " to " + square_representation[get_move_target(best_move)])
        print_board()

        boards.append(board)

        for pastboard in boards:
            if boards.count(pastboard) >= 3:
                Remi = True
                checkmate = True
        if checkmate == False:
            checkmate = check_mate()

        #inp = input(" ")
        #time.sleep(2)

        #make next move

    
    if Remi == True:
        print("Remi")
    else:
        print("Checkmate")


def main():
    allowed_time = 2

    load_fen(start_position)
    print_stats()
    print_board()
    testlist =[]
    print("\n")

    loop_game(3)
    #make the moves with depth 1
    
if __name__ == "__main__":
    main()
