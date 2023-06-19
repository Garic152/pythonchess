import numpy as np
import pickle

from main import make_move

white, black = range(2)

e, P, N, B, R, Q, K, p, n, b, r, q, k, o = range(14)

#source with explanation for the scores
#https://www.chessprogramming.org/Simplified_Evaluation_Function
pawn_value = 100
night_value = 320
bishop_value = 330
rook_value = 500
queen_value = 900

piece_values = np.array([0, 100, 320, 330, 500, 900, 20000, -100, -320, -330, -500, -900, -20000, 0])

mg_pawn_white = np.array([ 
    0,   0,   0,   0,   0,   0,  0,   0,         1,2,3,4,5,6,7,8,       
     98, 134,  61,  95,  68, 126, 34, -11,       1,2,3,4,5,6,7,8,       
     -6,   7,  26,  31,  65,  56, 25, -20,       1,2,3,4,5,6,7,8,       
    -14,  13,   6,  21,  23,  12, 17, -23,       1,2,3,4,5,6,7,8,       
    -27,  -2,  -5,  12,  17,   6, 10, -25,       1,2,3,4,5,6,7,8,       
    -26,  -4,  -4, -10,   3,   3, 33, -12,       1,2,3,4,5,6,7,8,       
    -35,  -1, -20, -23, -15,  24, 38, -22,       1,2,3,4,5,6,7,8,       
      0,   0,   0,   0,   0,   0,  0,   0,       1,2,3,4,5,6,7,8,            ])


mg_pawn_black = np.array([
    0,    0,    0,  0,  0,    0,     0, 0,        1,2,3,4,5,6,7,8,      
    -22,   38, 24, -15, -23,  -20,  -1, -35,      1,2,3,4,5,6,7,8,         
    -12,   33, 3,   3,  -10,  -4,   -4, -26,      1,2,3,4,5,6,7,8,         
    -25,   10, 6,   17,  12,  -5,   -2, -27,      1,2,3,4,5,6,7,8,         
    -23,   17, 12,  23,  21,   6,   13, -14,      1,2,3,4,5,6,7,8,         
    -20,   25, 56,  65,  31,   26,  7, -6,        1,2,3,4,5,6,7,8,      
    -11,   34, 126, 68,  95,   61,  134, 98,      1,2,3,4,5,6,7,8,         
    0,    0,    0,  0,   0,     0,   0,  0,        1,2,3,4,5,6,7,8,            ])

mg_night_white = np.array([
    -167, -89, -34, -49,  61, -97, -15, -107,       1,2,3,4,5,6,7,8,                
     -73, -41,  72,  36,  23,  62,   7,  -17,       1,2,3,4,5,6,7,8,                
     -47,  60,  37,  65,  84, 129,  73,   44,       1,2,3,4,5,6,7,8,                
      -9,  17,  19,  53,  37,  69,  18,   22,       1,2,3,4,5,6,7,8,                
     -13,   4,  16,  13,  28,  19,  21,   -8,       1,2,3,4,5,6,7,8,                
     -23,  -9,  12,  10,  19,  17,  25,  -16,       1,2,3,4,5,6,7,8,                
     -29, -53, -12,  -3,  -1,  18, -14,  -19,       1,2,3,4,5,6,7,8,                
    -105, -21, -58, -33, -17, -28, -19,  -23,       1,2,3,4,5,6,7,8,                 ])

mg_night_black = np.array([
    -23,     -19,-28, -17, -33,   -58, -21, -105,        1,2,3,4,5,6,7,8,                  
    -19,    -14, 18,  -1,   -3,   -12, -53, -29,         1,2,3,4,5,6,7,8,                 
    -16,     25, 17,  19,   10,   12, -9,   -23,         1,2,3,4,5,6,7,8,                 
    -8,     21,  19,  28,   13,   16, 4,    -13,         1,2,3,4,5,6,7,8,                 
    22,     18,  69,  37,   53,   19, 17,   -9,          1,2,3,4,5,6,7,8,                 
    44,     73,  129, 84,   65,   37, 60,   -47,         1,2,3,4,5,6,7,8,                 
    -17,    7,  62,   23,   36,   72, -41,  -73,         1,2,3,4,5,6,7,8,                 
    -107, -15,  -97,  61,   -49, -34, -89,  -167,         1,2,3,4,5,6,7,8,                 ])

mg_bishop_white = np.array([
    -29,   4, -82, -37, -25, -42,   7,  -8,          1,2,3,4,5,6,7,8, 
    -26,  16, -18, -13,  30,  59,  18, -47,          1,2,3,4,5,6,7,8, 
    -16,  37,  43,  40,  35,  50,  37,  -2,          1,2,3,4,5,6,7,8, 
     -4,   5,  19,  50,  37,  37,   7,  -2,          1,2,3,4,5,6,7,8, 
     -6,  13,  13,  26,  34,  12,  10,   4,          1,2,3,4,5,6,7,8, 
      0,  15,  15,  15,  14,  27,  18,  10,          1,2,3,4,5,6,7,8, 
      4,  15,  16,   0,   7,  21,  33,   1,          1,2,3,4,5,6,7,8, 
    -33,  -3, -14, -21, -13, -12, -39, -21,          1,2,3,4,5,6,7,8, 
])

mg_bishop_black = np.array([
    -21, -39, -12, -13, -21, -14, -3, -33,           1,2,3,4,5,6,7,8,               
    1, 33, 21, 7, 0, 16, 15, 4,                      1,2,3,4,5,6,7,8,       
    10, 18, 27, 14, 15, 15, 15, 0,                   1,2,3,4,5,6,7,8,       
    4, 10, 12, 34, 26, 13, 13, -6,                   1,2,3,4,5,6,7,8,       
    -2, 7, 37, 37, 50, 19, 5, -4,                    1,2,3,4,5,6,7,8,       
    -2, 37, 50, 35, 40, 43, 37, -16,                 1,2,3,4,5,6,7,8,           
    -47, 18, 59, 30, -13, -18, 16, -26,              1,2,3,4,5,6,7,8,               
    -8, 7, -42, -25, -37, -82, 4, -29,               1,2,3,4,5,6,7,8,           
])

mg_rook_white = np.array([
     32,  42,  32,  51, 63,  9,  31,  43,            1,2,3,4,5,6,7,8,       
     27,  32,  58,  62, 80, 67,  26,  44,            1,2,3,4,5,6,7,8,       
     -5,  19,  26,  36, 17, 45,  61,  16,            1,2,3,4,5,6,7,8,       
    -24, -11,   7,  26, 24, 35,  -8, -20,            1,2,3,4,5,6,7,8,       
    -36, -26, -12,  -1,  9, -7,   6, -23,            1,2,3,4,5,6,7,8,       
    -45, -25, -16, -17,  3,  0,  -5, -33,            1,2,3,4,5,6,7,8,       
    -44, -16, -20,  -9, -1, 11,  -6, -71,            1,2,3,4,5,6,7,8,       
    -19, -13,   1,  17, 16,  7, -37, -26,            1,2,3,4,5,6,7,8,       
])

mg_rook_black = np.array([
-26, -37, 7, 16, 17, 1, -13, -19,                    1,2,3,4,5,6,7,8,       
-71, -6, 11, -1, -9, -20, -16, -44,                  1,2,3,4,5,6,7,8,           
-33, -5, 0, 3, -17, -16, -25, -45,                   1,2,3,4,5,6,7,8,       
-23, 6, -7, 9, -1, -12, -26, -36,                    1,2,3,4,5,6,7,8,       
-20, -8, 35, 24, 26, 7, -11, -24,                    1,2,3,4,5,6,7,8,       
16, 61, 45, 17, 36, 26, 19, -5,                      1,2,3,4,5,6,7,8,       
44, 26, 67, 80, 62, 58, 32, 27,                      1,2,3,4,5,6,7,8,       
43, 31, 9, 63, 51, 32, 42, 32,                       1,2,3,4,5,6,7,8,   
])


mg_queen_white = np.array([
    -28,   0,  29,  12,  59,  44,  43,  45,          1,2,3,4,5,6,7,8,               
    -24, -39,  -5,   1, -16,  57,  28,  54,          1,2,3,4,5,6,7,8,               
    -13, -17,   7,   8,  29,  56,  47,  57,          1,2,3,4,5,6,7,8,               
    -27, -27, -16, -16,  -1,  17,  -2,   1,          1,2,3,4,5,6,7,8,               
     -9, -26,  -9, -10,  -2,  -4,   3,  -3,          1,2,3,4,5,6,7,8,               
    -14,   2, -11,  -2,  -5,   2,  14,   5,          1,2,3,4,5,6,7,8,               
    -35,  -8,  11,   2,   8,  15,  -3,   1,          1,2,3,4,5,6,7,8,               
     -1, -18,  -9,  10, -15, -25, -31, -50,          1,2,3,4,5,6,7,8,               
])              

mg_queen_black = np.array([
    -50, -31, -25, -15, 10, -9, -18, -1,             1,2,3,4,5,6,7,8,                               
    1, -3, 15, 8, 2, 11, -8, -35,                    1,2,3,4,5,6,7,8,                       
    5, 14, 2, -5, -2, -11, 2, -14,                   1,2,3,4,5,6,7,8,                       
    -3, 3, -4, -2, -10, -9, -26, -9,                 1,2,3,4,5,6,7,8,                           
    1, -2, 17, -1, -16, -16, -27, -27,               1,2,3,4,5,6,7,8,                           
    57, 47, 56, 29, 8, 7, -17, -13,                  1,2,3,4,5,6,7,8,                           
    54, 28, 57, -16, 1, -5, -39, -24,                1,2,3,4,5,6,7,8,                           
    45, 43, 44, 59, 12, 29, 0, -28,                  1,2,3,4,5,6,7,8,                       
])

mg_king_white = np.array([
    -65,  23,  16, -15, -56, -34,   2,    13,       1,2,3,4,5,6,7,8,
     29,  -1, -20,  -7,  -8,  -4, -38,   -29,       1,2,3,4,5,6,7,8,
     -9,  24,   2, -16, -20,   6,  22,   -22,       1,2,3,4,5,6,7,8,
    -17, -20, -12, 1000,  1000, -25, -14,-36,       1,2,3,4,5,6,7,8,
    -49,  -1, -27, 1000, 1000, -44, -33, -51,       1,2,3,4,5,6,7,8,
    -14, -14, -22, -46, -44, -30, -15,   -27,       1,2,3,4,5,6,7,8,
      1,   7,  -8, -64, -43, -16,   9,    8,        1,2,3,4,5,6,7,8,
    -15,  36,  12, -54,   8, -28,  24,    14,       1,2,3,4,5,6,7,8,
])


mg_king_black = np.array([
    14, 24, -28, 8, -54, 12, 36, -15,               1,2,3,4,5,6,7,8,                    
    8, 9, -16, -43, -64, -8, 7, 1,                  1,2,3,4,5,6,7,8,                
    -27, -15, -30, -44, -46, -22, -14, -14,         1,2,3,4,5,6,7,8,                            
    -51, -33, -44, 1000, 1000, -27, -1, -49,        1,2,3,4,5,6,7,8,                            
    -36, -14, -25, 1000, 1000, -12, -20, -17,       1,2,3,4,5,6,7,8,                            
    -22, 22, 6, -20, -16, 2, 24, -9,                1,2,3,4,5,6,7,8,                    
    -29, -38, -4, -8, -7, -20, -1, 29,              1,2,3,4,5,6,7,8,                    
    13, 2, -34, -56, -15, 16, 23, -65,              1,2,3,4,5,6,7,8,                    
])

#currently not used
mg_tables = [0, #e is not a piece => no table for e
                     mg_pawn_white,
                     mg_night_white,
                     mg_bishop_white,
                     mg_rook_white,
                     mg_queen_white,
                     mg_king_white,
                     mg_pawn_black,
                     mg_night_black,
                     mg_bishop_black,
                     mg_rook_black,
                     mg_queen_black,
                     mg_king_black,
                     0] #o is not a piece => no table for o

#was using list(reversed(array)) to reverse the array
early_game_pawn_white = np.array([
    0,  0,  0,  0,  0,  0,  0,  0,  1,2,3,4,5,6,7,8,
    50, 50, 50, 50, 50, 50, 50, 50, 1,2,3,4,5,6,7,8,
    10, 10, 20, 30, 30, 20, 10, 10, 1,2,3,4,5,6,7,8,
     5,  5, 10, 25, 25, 10,  5,  5, 1,2,3,4,5,6,7,8,
     0,  0,  0, 20, 20,  0,  0,  0, 1,2,3,4,5,6,7,8,
     5, -5,-10,  0,  0,-10, -5,  5, 1,2,3,4,5,6,7,8,
     5, 10, 10,-20,-20, 10, 10,  5, 1,2,3,4,5,6,7,8,
     0,  0,  0,  0,  0,  0,  0,  0, 1,2,3,4,5,6,7,8
])

early_game_pawn_black = np.array([
    0,	0,	0,	0,	0,	 0,	0,	0,	1,2,3,4,5,6,7,8,
    5,	10,	10,	-20,-20,10,	10,	5,	1,2,3,4,5,6,7,8,
    5,	-5,	-10, 0,	0,  -10,-5,	5,	1,2,3,4,5,6,7,8,
    0,	0,	0,	20,	20, 0,	0,	0,	1,2,3,4,5,6,7,8,
    5,	5,	10,	25,	25,	10,	5,	5,	1,2,3,4,5,6,7,8,
    10,	10,	20,	30,	30,	20,	10,	10,	1,2,3,4,5,6,7,8,
    50,	50,	50,	50,	50,	50,	50,	50,	1,2,3,4,5,6,7,8,
    0,	0,	0,	0,	0,	0,	0,	0,  1,2,3,4,5,6,7,8
])

early_game_night_white = np.array([
    -50,-40,-30,-30,-30,-30,-40,-50,    1,2,3,4,5,6,7,8,
    -40,-20,  0,  0,  0,  0,-20,-40,    1,2,3,4,5,6,7,8,
    -30,  0, 10, 15, 15, 10,  0,-30,    1,2,3,4,5,6,7,8,
    -30,  5, 15, 20, 20, 15,  5,-30,    1,2,3,4,5,6,7,8,
    -30,  0, 15, 20, 20, 15,  0,-30,    1,2,3,4,5,6,7,8,
    -30,  5, 10, 15, 15, 10,  5,-30,    1,2,3,4,5,6,7,8,
    -40,-20,  0,  5,  5,  0,-20,-40,    1,2,3,4,5,6,7,8,
    -50,-40,-30,-30,-30,-30,-40,-50,    1,2,3,4,5,6,7,8
])
early_game_night_black= np.array([
    -50, -40,-30, -30,-30,-30, -40, -50,    1,2,3,4,5,6,7,8,
    -40, -20,  0,   5,  5, 0, -20,  -40,    1,2,3,4,5,6,7,8,
    -30,   5, 10,  15, 15, 10,  5,  -30,    1,2,3,4,5,6,7,8,
    -30,   0, 15,  20, 20, 15,  0,  -30,    1,2,3,4,5,6,7,8,
    -30,   5, 15,  20, 20, 15,  5,  -30,    1,2,3,4,5,6,7,8,
    -30,   0, 10,  15, 15, 10,  0,  -30,    1,2,3,4,5,6,7,8,
    -40, -20,  0,   0,  0,  0, -20, -40,    1,2,3,4,5,6,7,8,
    -50, -40,-30, -30,-30,-30, -40, -50,    1,2,3,4,5,6,7,8

])
early_game_bishop_white = np.array([
    -20,-10,-10,-10,-10,-10,-10,-20,        1,2,3,4,5,6,7,8,
    -10,  0,  0,  0,  0,  0,  0,-10,        1,2,3,4,5,6,7,8,
    -10,  0,  5, 10, 10,  5,  0,-10,        1,2,3,4,5,6,7,8,
    -10,  5,  5, 10, 10,  5,  5,-10,        1,2,3,4,5,6,7,8,
    -10,  0, 10, 10, 10, 10,  0,-10,        1,2,3,4,5,6,7,8,
    -10, 10, 10, 10, 10, 10, 10,-10,        1,2,3,4,5,6,7,8,
    -10,  5,  0,  0,  0,  0,  5,-10,        1,2,3,4,5,6,7,8,
    -20,-10,-10,-10,-10,-10,-10,-20,        1,2,3,4,5,6,7,8
])
early_game_bishop_black = np.array([
      -20, -10, -10, -10, -10, -10, -10,-20,    8, 7, 6, 5, 4, 3, 2, 1, 
      -10,   5,   0,   0,   0,  0,   5, -10,    8, 7, 6, 5, 4, 3, 2, 1, 
      -10,  10,  10,  10,  10, 10,  10, -10,    8, 7, 6, 5, 4, 3, 2, 1, 
      -10,   0,  10,  10,  10, 10,   0, -10,    8, 7, 6, 5, 4, 3, 2, 1, 
      -10,   5,   5,  10,  10,  5,   5, -10,    8, 7, 6, 5, 4, 3, 2, 1, 
      -10,   0,   5,  10,  10,  5,   0, -10,    8, 7, 6, 5, 4, 3, 2, 1, 
      -10,   0,   0,   0,   0,  0,   0, -10,    8, 7, 6, 5, 4, 3, 2, 1, 
      -20, -10, -10, -10, -10, -10, -10,-20,    8, 7, 6, 5, 4, 3, 2, 1, 
])

early_game_rook_white = np.array([
    0,  0,  0,  0,  0,  0,  0,  0,      1,2,3,4,5,6,7,8,
     5, 10, 10, 10, 10, 10, 10,  5,     1,2,3,4,5,6,7,8,
    -5,  0,  0,  0,  0,  0,  0, -5,     1,2,3,4,5,6,7,8,
    -5,  0,  0,  0,  0,  0,  0, -5,     1,2,3,4,5,6,7,8,
    -5,  0,  0,  0,  0,  0,  0, -5,     1,2,3,4,5,6,7,8,
    -5,  0,  0,  0,  0,  0,  0, -5,     1,2,3,4,5,6,7,8,
    -5,  0,  0,  0,  0,  0,  0, -5,     1,2,3,4,5,6,7,8,
     0,  0,  0,  5,  5,  0,  0,  0,     1,2,3,4,5,6,7,8
])

early_game_rook_black = np.array([
     0, 0, 0, 5, 5, 0, 0, 0,      8, 7, 6, 5, 4, 3, 2, 1,
    -5, 0, 0, 0, 0, 0, 0,-5,      8, 7, 6, 5, 4, 3, 2, 1,
    -5, 0, 0, 0, 0, 0, 0,-5,      8, 7, 6, 5, 4, 3, 2, 1,
    -5, 0, 0, 0, 0, 0, 0,-5,      8, 7, 6, 5, 4, 3, 2, 1,
    -5, 0, 0, 0, 0, 0, 0,-5,      8, 7, 6, 5, 4, 3, 2, 1,
    -5, 0, 0, 0, 0, 0, 0,-5,      8, 7, 6, 5, 4, 3, 2, 1,
    5, 10,10,10,10,10,10, 5,      8, 7, 6, 5, 4, 3, 2, 1,
    0,  0, 0, 0, 0, 0, 0, 0,      8, 7, 6, 5, 4, 3, 2, 1
])

early_game_queen_white = np.array([
    -20,-10,-10, -5, -5,-10,-10,-20,    1,2,3,4,5,6,7,8,
    -10,  0,  0,  0,  0,  0,  0,-10,    1,2,3,4,5,6,7,8,
    -10,  0,  5,  5,  5,  5,  0,-10,    1,2,3,4,5,6,7,8,
     -5,  0,  5,  5,  5,  5,  0, -5,    1,2,3,4,5,6,7,8,
      0,  0,  5,  5,  5,  5,  0, -5,    1,2,3,4,5,6,7,8,
    -10,  5,  5,  5,  5,  5,  0,-10,    1,2,3,4,5,6,7,8,
    -10,  0,  5,  0,  0,  0,  0,-10,    1,2,3,4,5,6,7,8,
    -20,-10,-10, -5, -5,-10,-10,-20,    1,2,3,4,5,6,7,8
])

early_game_queen_black = np.array([
-20,-10,-10,-5,-5,-10,-10,-20,  8, 7, 6, 5, 4, 3, 2, 1, 
-10, 0,  0,  0, 0, 5,  0, -10,  8, 7, 6, 5, 4, 3, 2, 1, 
-10, 0,  5,  5, 5, 5,  5, -10,  8, 7, 6, 5, 4, 3, 2, 1, 
-5,  0,  5,  5, 5, 5,  0,  -5,  8, 7, 6, 5, 4, 3, 2, 1, 
-5,  0,  5,  5, 5, 5,  0,  -5,  8, 7, 6, 5, 4, 3, 2, 1, 
-10, 0,  5,  5, 5, 5,  0, -10,  8, 7, 6, 5, 4, 3, 2, 1, 
-10, 0,  0,  0, 0, 0,  0, -10,  8, 7, 6, 5, 4, 3, 2, 1, 
-20,-10,-10,-5,-5,-10,-10,-20,  8, 7, 6, 5, 4, 3, 2, 1 
])

early_game_king_white = np.array([
    -30,-40,-40,-50,-50,-40,-40,-30,    1,2,3,4,5,6,7,8,
    -30,-40,-40,-50,-50,-40,-40,-30,    1,2,3,4,5,6,7,8,
    -30,-40,-40,-50,-50,-40,-40,-30,    1,2,3,4,5,6,7,8,
    -30,-40,-40,-50,-50,-40,-40,-30,    1,2,3,4,5,6,7,8,
    -20,-30,-30,-40,-40,-30,-30,-20,    1,2,3,4,5,6,7,8,
    -10,-20,-20,-20,-20,-20,-20,-10,    1,2,3,4,5,6,7,8,
     20, 20,  0,  0,  0,  0, 20, 20,    1,2,3,4,5,6,7,8,
     20, 30, 10,  0,  0, 10, 30, 20,    1,2,3,4,5,6,7,8
])

eg_king_table = np.array([
        -74, -35, -18, -18, -11, 15, 4, -17,
        -12, 17, 14, 17, 17, 38, 23, 11,
        10, 17, 23, 15, 20, 45, 44, 13,
        -8, 22, 24, 75, 65, 33, 26, 3,
        -18, -4, 21, 125, 135, 23, 9, -11,
        -19, -3, 11, 21, 23, 16, 7, -9,
        -27, -11, 4, 13, 14, 4, -5, -17,
        -53, -34, -21, -11, -28, -14, -24, -43,
])

early_game_king_white_2 = np.array([
    -30,-40,-40,-50,-50,-40,-40,-30,    1,2,3,4,5,6,7,8,
    -30,-40,-40,-50,-50,-40,-40,-30,    1,2,3,4,5,6,7,8,
    -30,-40,-40,-50,-50,-40,-40,-30,    1,2,3,4,5,6,7,8,
    -30,-40,-40,-50,-50,-40,-40,-30,    1,2,3,4,5,6,7,8,
    -20,-30,-30,-40,-40,-30,-30,-20,    1,2,3,4,5,6,7,8,
    -10,-20,-20,-20,-20,-20,-20,-10,    1,2,3,4,5,6,7,8,
     5, 5,  10, 10, 10, 10, 5, 5,    1,2,3,4,5,6,7,8,
    -20,-10, 0,  0,  0, 0, -10,-20,    1,2,3,4,5,6,7,8
])

early_game_king_black = np.array([
     20,  30,  10,   0,   0,  10,  30,  20,      8, 7, 6, 5, 4, 3, 2, 1,
     20,  20,   0,   0,   0,   0,  20,  20,      8, 7, 6, 5, 4, 3, 2, 1,
    -10, -20, -20, -20, -20, -20, -20, -10,      8, 7, 6, 5, 4, 3, 2, 1,
    -20, -30, -30, -40, -40, -30, -30, -20,      8, 7, 6, 5, 4, 3, 2, 1,
    -30, -40, -40, -50, -50, -40, -40, -30,      8, 7, 6, 5, 4, 3, 2, 1,
    -30, -40, -40, -50, -50, -40, -40, -30,      8, 7, 6, 5, 4, 3, 2, 1,
    -30, -40, -40, -50, -50, -40, -40, -30,      8, 7, 6, 5, 4, 3, 2, 1,
    -30, -40, -40, -50, -50, -40, -40, -30,      8, 7, 6, 5, 4, 3, 2, 1
])


eg_king_table = [
        -74, -35, -18, -18, -11, 15, 4, -17,
        -12, 17, 14, 17, 17, 38, 23, 11,
        10, 17, 23, 15, 20, 45, 44, 13,
        -8, 22, 24, 75, 65, 33, 26, 3,
        -18, -4, 21, 125, 135, 23, 9, -11,
        -19, -3, 11, 21, 23, 16, 7, -9,
        -27, -11, 4, 13, 14, 4, -5, -17,
        -53, -34, -21, -11, -28, -14, -24, -43,
]


def evaluate(board, side):
    local_board = np.array(board.board)
    return count_material(local_board, side) + consider_positions(local_board, side)


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
    #maybe if turn < 10 then evaluate with early_game tables else with middle_game
    perspective = 1 if side == white else -1
    for position in range(len(board)):
        piece = board[position]
        if piece > 0 and piece < 7:
            val_pos += early_game_tables[piece][position]
        elif piece > 6 and piece < 13:
            val_pos -= early_game_tables[piece][position]

    return val_pos*perspective

#                  e,   P,            N,            B,          R,          Q,          K, \n p, n, b, r, q, k, o = range(14)
material_values = [0, pawn_value, night_value, bishop_value, rook_value, queen_value, 20000, 
                     -pawn_value, -night_value, -bishop_value, -rook_value, -queen_value, -20000, 0,0,0] # we get sometimes figure on position 127 with value 15 that is why we have two extra zeros in the end

def count_material(local_board, side):
    perspective = 1 if side == white else -1

    val = np.sum(piece_values[local_board])

    return val*perspective


def sort_moves(board, move):
    value = 0

    board_copy = pickle.dumps(board)

    if not make_move(move, board):
        board = pickle.loads(board_copy)
        pass

    for piece in board.board:
        if piece < 13 and piece > 0:
            value += piece_values[piece]

    board = pickle.loads(board_copy)

    return value
