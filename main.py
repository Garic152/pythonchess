"""
Trying out some chess engine stuff
"""

from random import randrange
import time

import alphabeta

#defining the piece integer representation
e, P, N, B, R, Q, K, p, n, b, r, q, k, o = range(14)

white, black = range(2)

Castling = {'KC': 1, 'QC': 2, 'kc': 4, 'qc': 8}


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

#from ascii to normal chars
char_pieces = {'P': P, 'N': N, 'B': B, 'R': R, 'Q': Q, 'K': K, 'p': p, 'n': n, 'b': b, 'r': r, 'q': q, 'k': k}
promoted_pieces = {Q: 'q', R: 'r', B: 'b', N: 'n', q: 'q', r: 'r', b: 'b', n: 'n'}


start_position = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
fen = 'r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1'



#castling rights in bit representation, where 15 is 1111, meaning both sides can castle both on the queen and king side
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

#board information class
class Board:
    def __init__(self):
        self.board = [
        r, n, b, q, k, b, n, r, o, o, o, o, o, o, o, o,
        p, p, p, p, p, p, p, p, o, o, o, o, o, o, o, o,
        e, e, e, e, e, e, e, e, o, o, o, o, o, o, o, o,
        e, e, e, e, e, e, e, e, o, o, o, o, o, o, o, o,
        e, e, e, e, e, e, e, e, o, o, o, o, o, o, o, o,
        e, e, e, e, e, e, e, e, o, o, o, o, o, o, o, o,
        P, P, P, P, P, P, P, P, o, o, o, o, o, o, o, o,
        R, N, B, Q, K, B, N, R, o, o, o, o, o, o, o, o
        ]

        self.king_position = [116, 4]
        self.side = white
        self.can_castle = 0
        self.countercheck = 0

        #define board state copy variable
        self.board_copy = [0] * 128
        self.king_position_copy = [2]
        self.side_copy = 0
        self.can_castle_copy = 0

    def copy_move(self):
        #copy board state
        self.board_copy = self.board.copy()
        self.king_position_copy = self.king_position.copy()
        self.side_copy = self.side
        self.can_castle_copy = self.can_castle


    def undo_move(self):
        #undo board state
        self.board = self.board_copy.copy()
        self.king_position = self.king_position_copy.copy()
        self.side = self.side_copy
        self.can_castle = self.can_castle_copy

        #reset copy variables
        self.board_copy = [0] * 128
        self.king_position_copy = [2]
        self.side_copy = 0
        self.can_castle_copy = 0


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


def clear_board(board):
    # loop over column
    for rank in range(8):
        # loop over row
        for file in range(16):
            position = file + rank * 16
            # check if the piece is on the field
            if not position & 0x88:
                # clears the board
                board.board[position] = e

def print_board(board):
    # loop over column
    for rank in range(8):
        # loop over row
        for file in range(16):
            if file == 0:
                print(8 - rank, end="   ")
            position = file + rank * 16
            # check if the piece is on the field
            if not position & 0x88:
                print(char_ascii[board.board[position]], end=" ")
        print(end="\n")
    print("\n    A B C D E F G H")


def is_position_attacked(position, board, side):
    # attacked by pawn
    if not side:
        if not ((position + 17) & 0x88) and board.board[position + 17] == P:
            return True
        elif not ((position + 15) & 0x88) and board.board[position + 15] == P:
            return True
    else:
        if not ((position - 17) & 0x88) and board.board[position - 17] == p:
            return True
        elif not ((position - 15) & 0x88) and board.board[position - 15] == p:
            return True

    # attacked by knight
    if not side:
        for move in knight_movement:
            if not ((position + move) & 0x88) and board.board[position + move] == N:
                return True
    else:
        for move in knight_movement:
            if not ((position + move) & 0x88) and board.board[position + move] == n:
                return True

    # attacked by king
    if not side:
        for move in king_movement:
            if not ((position + move) & 0x88) and board.board[position + move] == K:
                return True
    else:
        for move in king_movement:
            if not ((position + move) & 0x88) and board.board[position + move] == k:
                return True


    # attacked by Bishop and Queen
    for move in bishop_movement:
        # creates new temp position
        new_position = position + move

        # loop through all the available positions for one move
        while not ((new_position) & 0x88):
            # grabs the piece at current position

            target = board.board[new_position]

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
            target = board.board[new_position]

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

def print_attack(board):
    # loop over column
    for rank in range(8):
        # loop over row
        for file in range(16):
            if file == 0:
                print(rank + 1, end="   ")
            position = file + rank * 16
            # check if the piece is on the field
            if not position & 0x88:
                print("x" if is_position_attacked(position, board) else ".", end=" ")
        print(end="\n")
    print("\n    A B C D E F G H")


def print_stats(board):
    print("Side to move: " + char_sides[board.side])
    print("Castling: " + str(bin(board.can_castle)[2:]).rjust(4, "0"))


def load_fen(fen, board):
    fen_position = 0

    # reset board
    clear_board(board)

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
                        board.king_position[white] = position
                
                    elif (fen[fen_position] == 'k'):
                        board.king_position[black] = position


                    # set current board position to fen piece
                    board.board[position] = char_pieces[fen[fen_position]]

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
    board.side = white if fen[fen_position] == "w" else black

    # go to castling position
    fen_position += 2

    while fen[fen_position] != " ":
        if fen[fen_position] == "K":
            board.can_castle |= Castling["KC"]
        elif fen[fen_position] == "Q":
            board.can_castle |= Castling["QC"]
        elif fen[fen_position] == "k":
            board.can_castle |= Castling["kc"]
        elif fen[fen_position] == "q":
            board.can_castle |= Castling["qc"]
        elif fen[fen_position] == "-":
            break
        fen_position += 1


# move generation
def generate_move(move, board):
    # loop over all positions on the board
    for position in range(128):
        if not position & 0x88:
            # white moves
            if not board.side:
                # pawn moves + captures
                if board.board[position] == P:
                    # move forward
                    if not (position - 16) & 0x88 and not board.board[position - 16]:
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
                            if (position > 95 and position < 104) and not board.board[
                                position - 32
                            ]:
                                #move 2 squares ahead
                                move.add_move(set_move(position, position - 32, 0, 0, 1, 0))

                    # pawn capture moves
                    for movement in bishop_movement:
                        if (
                            not (position - movement) & 0x88
                            and board.board[position - movement]
                            and movement > 0
                            and board.board[position - movement] > 6
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
                if board.board[position] == K:
                    # check king side castle
                    if (
                        board.can_castle & Castling["KC"]
                        and position == 116
                        and not board.board[117]
                        and not board.board[118]
                        and board.board[119] == R
                    ):
                        # temp variable to check if any pieces king side are attacked
                        is_attacked = False
                        for i in range(116, 119):
                            if is_position_attacked(i, board, black):
                                is_attacked = True

                        if not is_attacked:
                            pass
                            move.add_move(set_move(116, 118, 0, 0, 0, 1))

                    # check queen side castle
                    if (
                        board.can_castle & Castling["QC"]
                        and position == 116
                        and not board.board[115]
                        and not board.board[114]
                        and not board.board[113]
                        and board.board[112] == R
                    ):
                        # temp variable to check if any pieces king side are attacked
                        is_attacked = False
                        for i in range(113, 117):
                            if is_position_attacked(i, board, black):
                                is_attacked = True

                        if not is_attacked:
                            pass
                            move.add_move(set_move(116, 114, 0, 0, 0, 1))

            # black moves
            else:
                # pawn moves + captures
                if board.board[position] == p:
                    if not (position + 16) & 0x88 and not board.board[position + 16]:
                        if position > 95 and position < 104:
                            pass
                            move.add_move(set_move(position, position + 16, q, 0, 0, 0))
                            move.add_move(set_move(position, position + 16, r, 0, 0, 0))
                            move.add_move(set_move(position, position + 16, b, 0, 0, 0))
                            move.add_move(set_move(position, position + 16, n, 0, 0, 0))

                        else:
                            pass
                            move.add_move(set_move(position, position + 16, 0, 0, 0, 0))

                            if (position > 15 and position < 24) and not board.board[
                                position + 32
                            ]:
                                pass
                                move.add_move(set_move(position, position + 32, 0, 0, 1, 0))

                    for movement in bishop_movement:
                        if (
                            not (position - movement) & 0x88
                            and board.board[position - movement]
                            and movement < 0
                            and board.board[position - movement] < 7
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
                if board.board[position] == k:
                    if (
                        board.can_castle & Castling["kc"]
                        and position == 4
                        and not board.board[5]
                        and not board.board[6]
                        and board.board[7] == r
                    ):
                        is_attacked = False
                        for i in range(4, 7):
                            if is_position_attacked(i, board, white):
                                is_attacked = True

                        if not is_attacked:
                            pass
                            move.add_move(set_move(4, 6, 0, 0, 0, 1))

                    if (
                        board.can_castle & Castling["qc"]
                        and position == 4
                        and not board.board[3]
                        and not board.board[2]
                        and not board.board[1]
                        and board.board[0] == r
                    ):
                        is_attacked = False
                        for i in range(1, 5):
                            if is_position_attacked(i, board, white):
                                is_attacked = True

                        if not is_attacked:
                            pass
                            move.add_move(set_move(4, 2, 0, 0, 0, 1))

            # knight moves and captures
            if (board.board[position] == N) if not board.side else (board.board[position] == n):
                # loop over knight moves
                for movement in knight_movement:
                    # check if targeted square is on board
                    if not (position + movement) & 0x88:
                        # safe target piece for capture checks
                        target = board.board[position + movement]

                        # 2 situations for either white or black pieces
                        if (
                            (not target or (target >= 7 and target <= 12))
                            if not board.side
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
            if (board.board[position] == K) if not board.side else (board.board[position] == k):
                for movement in king_movement:
                    if not (position + movement) & 0x88:
                        target = board.board[position + movement]

                        if (
                            (not target or (target >= 7 and target <= 12))
                            if not board.side
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
                ((board.board[position] == B) or (board.board[position] == Q))
                if not board.side
                else ((board.board[position] == b) or (board.board[position] == q))
            ):
                # loop over bishop and queen moves
                for movement in bishop_movement:
                    # safe target square and increment
                    target = position + movement

                    current_movement = movement
                    while not target & 0x88:
                        # get piece at targeted position
                        piece = board.board[target]

                        # if it hits own piece
                        if (
                            (piece >= 1 and piece <= 6)
                            if not board.side
                            else (piece >= 7 and piece <= 12)
                        ):
                            break

                        # if it hits opponent piece
                        if (
                            (piece >= 7 and piece <= 12)
                            if not board.side
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
                ((board.board[position] == R) or (board.board[position] == Q))
                if not board.side
                else ((board.board[position] == r) or (board.board[position] == q))
            ):
                for movement in rook_movement:
                    target = position + movement
                    current_movement = movement

                    while not target & 0x88:
                        piece = board.board[target]

                        if (
                            (piece >= 1 and piece <= 6)
                            if not board.side
                            else (piece >= 7 and piece <= 12)
                        ):
                            break

                        if (
                            (piece >= 7 and piece <= 12)
                            if not board.side
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
def make_move(move, board):
    board.copy_move()

    #get current and target position
    position = get_move_source(move)
    target = get_move_target(move)
    promoted_piece = get_move_piece(move)
    castling = get_move_castling(move)

    #if target is king
    if board.board[target] == K or board.board[target] == k:
        return 0

    #make the move
    board.board[target] = board.board[position]
    board.board[position] = e

    #promote pawn
    if promoted_piece:
        board.board[target] = promoted_piece

    #update king position
    if board.board[position] == K or board.board[position] == k:
        board.king_position[side] = target

    #castling moves
    if castling:
        match target:
            case 118:
                board.board[117] = board.board[119]
                board.board[119] = e
            case 6:
                board.board[5] = board.board[7]
                board.board[7] = e
            case 114:
                board.board[115] = board.board[112]
                board.board[112] = e
            case 2:
                board.board[3] = board.board[0]
                board.board[0] = e

    #change castling rights
    board.can_castle &= castling_rights[position]
    board.can_castle &= castling_rights[target]

    #change side
    board.side ^= 1

    #print("Moving " + square_representation[position] + " to " + square_representation[target])

    #is king attacked
    if is_position_attacked(board.king_position[board.side^1], board, board.side):
        #undo move 
        board.undo_move()
        return 0

    else:
        #legal move

        return 1


#define tree length
tree_size = 0

def get_time_ms():
    return time.process_time() 

def chess(depth, board):
    global tree_size
    #break when depth = 0
    if not depth:
        tree_size += 1
        return

    #generate move
    moves = Moves()

    moves.count = 0

    generate_move(moves, board)

    for move in moves:
        board.copy_move()

        #only legal moves
        if not make_move(move, board):
            continue

        #recursive until depth = 0
        chess(depth - 1, board)
        
        board.undo_move()

    
def chess_perft(depth, board):
    #generate move
    moves = Moves()
    #moves.count = 0
    generate_move(moves, board)
    print(moves)

    for move in moves:
        board.copy_move()

        #only legal moves
        if not make_move(move, board):
            continue

        #recursive until depth = 0
        chess(depth - 1, board)
        
        board.undo_move()

    return moves[randrange(0, moves.count)]


def check_mate(board):
    global tree_size
    moves = Moves()
    # moves.count = 0
    generate_move(moves, board)
    checklist = []
    for move in moves:
        board.copy_move()

        if not make_move(move, board):
            continue
        checklist.append(move)

        board.undo_move()
    return checklist == []

#loop over game
def loop_game(depth, allowed_time, board):
    checkmate = False
    remi = False
    boards = []
    while not checkmate:

        #get and make best move
        #best_move = alphabeta.minimax(allowed_time, depth, board)
        best_move = chess_perft(depth, board)
        make_move(best_move, board)

        #print best move and board
        print("Best move: " + char_ascii[board.board[get_move_target(best_move)]] + " on "  + square_representation[get_move_source(best_move)] + " to " + square_representation[get_move_target(best_move)])
        print_board(board)
        inp = input(" ")
        boards.append(board.board)
        for pastboard in boards:
            if boards.count(pastboard) >= 3:
                remi = True
                checkmate = True
        if not checkmate:
            checkmate = check_mate(board)
    if remi:
        print("Remi")
    else:
        print("Checkmate")


def main():
    starttime = get_time_ms()
    board = Board()

    allowed_time = 2
    load_fen(start_position, board)
    print_stats(board)
    print_board(board)
    #testlist =[]
    #print("\n")

    loop_game(2, allowed_time, board)

    print(tree_size)
    #make the moves with depth 1


    # safe Benchmark
    with open("benchmark.txt", 'w') as my_file:
        my_file.write('With FEN: ' + start_position + '\n')
        my_file.write('Runtime = ' + str(get_time_ms() - starttime))


if __name__ == "__main__":
    main()
