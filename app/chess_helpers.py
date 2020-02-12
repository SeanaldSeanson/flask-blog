from flask import session
import os, sqlite3, re
from app.blog_helpers import sql_execute, sql_query

wK = '\u2654'
wQ = '\u2655'
wR = '\u2656'
wB = '\u2657'
wN = '\u2658'
wP = '\u2659'
bK = '\u265A'
bQ = '\u265B'
bR = '\u265C'
bB = '\u265D'
bN = '\u265E'
bP = '\u265F'

def is_valid_move_syntax(move):
    move_pattern = re.compile('[a-zA-Z][0-8][ ,]+[a-zA-Z][0-8]')
    if move_pattern.match(move):
        return True
    return False

def is_valid_move(move, game_id):
    move = unpack_move(move)
    board = build_board(game_id)
    valid_moves = get_valid_moves(board, move[0][0], move[0][1])
    for i in valid_moves:
        if i == (move[1][0], move[1][1]):
            return True
    return False
        
def unpack_move(move):
    startX = int(move[:1].upper()) - 65
    startY = int(move[:2].upper()) - 65
    endX = int(move[-1:].upper()) - 65
    endY = int(move[-2:].upper()) - 65
    return ((startX, startY), (endX, endY))

def submit_move(move, game_id):
    turn = sql_query('SELECT TOP 1 turn FROM chessMoves WHERE gameId=? ORDER BY turn DESC)', game_id).fetchone()[0]
    turn += 1

    if is_valid_move(move, game_id):
        pass # insert move

def get_moves(game_id):
    return sql_query('SELECT * FROM chessMoves WHERE gameId=? ORDER BY turn ASC', game_id)

# def build_board_txt(moves):
#     return 'insert board here'
#     game_record = sql_query('SELECT * FROM chessGames WHERE id=?', game_id)[0]
#     moves = sql_query('SELECT * FROM chessMoves WHERE gameId=?', game_id)
#     for record in moves:
#         pass

def build_board(game_id):
    # Initialize board
    board = []
    board.append([bR,bN,bB,bK,bQ,bB,bN,bR])
    board.append([bP,bP,bP,bP,bP,bP,bP,bP])
    for i in range(2, 6):
        board.append([])
        for j in range(8):
            board[i].append(' ')
    board.append([wP,wP,wP,wP,wP,wP,wP,wP])
    board.append([wR,wN,wB,wK,wQ,wB,wN,wR])

    for m in get_moves(game_id):
        startX, startY = (m[3], m[4])
        endX, endY = (m[5], m[6])
        piece = board[startX][startY]
        board[startX][startY] = ' '
        board[endX][endY] = piece
    
    return board

def piece_type(p):
    if p == wK or p == bK:
        return 'K'
    if p == wQ or p == bQ:
        return 'Q'
    if p == wB or p == bB:
        return 'B'
    if p == wN or p == bN:
        return 'N'
    if p == wR or p == bR:
        return 'R'
    return ' '

def trace_path(board, startX, startY, dirX, dirY, max_len=8):
    x, y = startX, startY
    points = []
    points.append((x,y))
    dist = 0
    while x > 0 and x < 8 and y > 0 and x < 8 and dist < max_len and board[x][y] == ' ':
        x += dirX
        y += dirY
        points.append((x, y))
        dist += 1
    return points

def board_txt(game_id):
    board = build_board(game_id)
    row_line = '---------------------------------\n'
    txt = ''
    for i in range(len(board)):
        txt += row_line
        for j in board[i]:
            txt += '| ' + j + ' '
        txt += '|\n'
    txt += row_line

    return txt

def get_valid_moves(board, startX, startY):
    piece = board[startY][startX]
    ptype = piece_type(piece)
    moves = []
    if ptype == 'K':
        for dirX in range(-1, 2):
            for dirY in range(-1, 2):
                moves += trace_path(board, startX, startY, dirX, dirY, 1)
        if startX == 3:
            can_castle = True
            for x in range(5, 7):
                if board[startY][x] == ' ':
                    can_castle = False
            if can_castle and piece_type(board[startY][7]) == 'R':
                moves.append((7, startY))
            
            can_castle = True
            for x in reversed(range(1, 4)):
                if board[startY][x] == ' ':
                    can_castle = False
            if can_castle and piece_type(board[startY][0]) == 'R':
                moves.append((0, startY))
        
        return moves
    if ptype == 'Q':
        for dirX in range(-1, 2):
            for dirY in range(-1, 2):
                moves += trace_path(board, startX, startY, dirX, dirY)
        return moves
    if ptype == 'B':
        for dirX in [-1, 1]:
            for dirY in [-1, 1]:
                moves += trace_path(board, startX, startY, dirX, dirY)
        return moves
    if ptype == 'N':
        if startX + 2 < 7:
            if startY + 1 < 7:
                moves.append((startX + 2, startY + 1))
            if startY - 1 > 0:
                moves.append((startX + 2, startY - 1))
        if startX - 2 > 0:
            if startY + 1 < 7:
                moves.append((startX - 2, startY + 1))
            if startY - 1 > 0:
                moves.append((startX - 2, startY - 1))
        if startY + 2 < 7:
            if startX + 1 < 7:
                moves.append((startX + 1, startY + 2))
            if startX - 1 > 0:
                moves.append((startX + 1, startY - 2))
        if startY - 2 > 0:
            if startX + 1 < 7:
                moves.append((startX + 1, startY - 2))
            if startX - 1 > 0:
                moves.append((startX - 1, startY - 2))
        return moves
    if ptype == 'R':
        for dirX in [-1, 1]:
            moves += trace_path(board, startX, startY, dirX, 0)
        for dirY in [-1, 1]:
            moves += trace_path(board, startX, startY, dirX, 0)
        return moves
    return moves