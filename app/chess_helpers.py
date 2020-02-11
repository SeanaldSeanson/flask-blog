from flask import session
import os, sqlite3, re
from app.blog_helpers import sql_execute, sql_query

wK = 'N\{WHITE CHESS KING}'
wQ = 'N\{WHITE CHESS QUEEN}'
wR = 'N\{WHITE CHESS ROOK}'
wB = 'N\{WHITE CHESS BISHOP}'
wN = 'N\{WHITE CHESS KNIGHT}'
wP = 'N\{WHITE CHESS PAWN}'
bK = 'N\{BLACK CHESS KING}'
bQ = 'N\{BLACK CHESS QUEEN}'
bR = 'N\{BLACK CHESS ROOK}'
bB = 'N\{BLACK CHESS BISHOP'
bN = 'N\{BLACK CHESS KNIGHT}'
bP = 'N\{BLACK CHESS PAWN}'

def is_valid_move_syntax(move):
    move_pattern = re.compile('[a-zA-Z][0-8][ ,]+[a-zA-Z][0-8]')
    if move_pattern.match(move):
        return True
    return False

def is_valid_move(move):
    pass


def unpack_move(move):
    return (move[:2], move[-2:])

def build_board_txt(moves):
    return 'insert board here'
    # game_record = sql_query('SELECT * FROM chessGames WHERE id=?', game_id)[0]
    moves = sql_query('SELECT * FROM chessMoves WHERE gameId=?', game_id)
    for record in moves:
        pass

def board_arr(moves):
    moves = sql_query('SELECT * FROM chessMoves WHERE gameId=?', game_id)

    board = [bR,bK,b
    for record in moves:
        