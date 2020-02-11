from flask import session
import os, sqlite3, re
from app.blog_helpers import sql_execute, sql_query

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

def board_dict(moves):
    moves = sql_query('SELECT * FROM chessMoves WHERE gameId=?', game_id)
    for record in moves:
        get