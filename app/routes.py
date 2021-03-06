from app import app
from markdown import markdown
from flask import render_template_string, request, session, redirect, url_for, escape, abort, send_from_directory, send_file
from app.blog_helpers import render_markdown, read_txt, write_txt, backup_page, is_admin, is_view, fill_page, login_text, sql_query, sql_execute, get_uid, get_uname
from app.chess_helpers import is_valid_move_syntax, submit_move, board_txt, player_turn
from glob import glob
from pathlib import PurePath
import os, sqlite3, secrets, hashlib

app.secret_key = '`(7h_B/G PH:=IyT-$L^mE~5AR!Y|?/;i=2z1]ESGMKRtg-f'

if __name__ == '__main__':
    app.run()
    # app.run(ssl_context='adhoc')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get user record from SQLite database user.db
        print(request.form['username'])
        udata = sql_query('SELECT * FROM users WHERE name=?', request.form['username'])[0]

        # Check hash from db against hash of salt + provided password
        if udata[3] == hashlib.sha256((udata[2] + request.form['password']).encode()).hexdigest():
            session['uid'] = udata[0]
            return redirect(url_for('index'))
        else:
            return render_page('login', foot='<p><font> color=red>Invalid Credentials</font></p>')

    return render_page('login')

@app.route('/logout')
def logout():
    if session:
        session.pop('uid', None)
        session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/')
@app.route('/index')
def index():
    return render_page('index')

# generic page
@app.route('/<view_name>')
def render_page(view_name, head = read_txt('bar.html', dir_path='app/views/parts'), foot=''):
    if is_view(view_name + '.html'):
        html = read_txt(view_name + '.html')
        return render_template_string(fill_page(html, head, foot), view_name = view_name, login = login_text())
    abort(404)

# edit generic page
@app.route('/edit/<view_name>', methods=['GET', 'POST'])
def edit_page(view_name):
    if session and is_admin(session['uid']):
        if request.method == 'POST':
            backup_page(view_name + '.html')
            write_txt(request.form['editor'], view_name + '.html')
            return redirect(url_for(view_name))

        html = read_txt('edit.html')
        if is_view(view_name + '.html'):
            view_name += '.html'
        else:
           abort(404)
        page = read_txt(view_name)
        return render_template_string(html, edit_name = view_name, editor_content = page, preview = '')
    else:
        abort(403)

@app.route('/all')
def all():
    html = read_txt('all.html')
    view_list = glob(os.path.normpath('app/views/*.html'))
    for p in view_list:
        html += '<p><a href=/' + PurePath(p).stem + '>' + PurePath(p).stem + '</a></p>\n'
    html = fill_page(html)
    return render_template_string(html, view_name = 'all', login = login_text())

@app.route('/chess')
def chess():
    html = read_txt('chess.html')
    html = fill_page(html)
    if session:

        html += '<p><a href=/chess/new>Start Game</a></p>'

        html += '<h2>Active Games</h2>'
        active_games = sql_query('SELECT * FROM chessGames WHERE (player1=? OR player2=?) AND start=1', session['uid'], session['uid'])

        if len(active_games) > 0:
            for g in active_games:
                html += '<p><a href=/chess/game/' + str(g[0]) + '>' + str(g[0]) + ': ' + get_uname(g[1]) + ' v. ' + get_uname(g[2]) + '</a></p>'
        else:
            html += 'No active games.'
        
        html += '\n<h2>Pending Games</h2>'
        pending_games = sql_query('SELECT * FROM chessGames WHERE (player1=? OR player2=?) AND start=0', session['uid'], session['uid'])
        if len(pending_games) > 0:
            for g in pending_games:
                html += '<p><a href=/chess/accept/' + str(g[0]) + '>' + str(g[0]) + ': ' + get_uname(g[1]) + ' v. ' + get_uname(g[2])
        else:
            html += 'No pending games.'
    else:
        html += '<p>You must log in to play chess.</p>'
    
    return render_template_string(html, view_name='chess', login = login_text())

@app.route('/chess/new', methods=['GET', 'POST'])
def chess_new():
    if session:
        if request.method == 'POST':
            if len(sql_query('SELECT uid users WHERE name=?', request.form['player'])) == 1:
                sql_execute('INSERT INTO chessGames (player1, player2, start) VALUES(?,?,0)', session['uid'], get_uid(request.form['player']))
            return redirect(url_for('chess'))
        else:
            return render_page('chess_new')
    else:
        abort(403)

@app.route('/chess/game/<game_id>', methods=['GET', 'POST'])
def chess_game(game_id):
    player1 = ''
    player2 = ''
    board = ''
    html = read_txt('chess_game.html', dir_path='app/views/parts')

    game_record = sql_query('SELECT * FROM chessGames WHERE id=?', game_id)
    if len(game_record) == 1:
        game_record = game_record[0]
        player1 = game_record[1]
        player2 = game_record[2]
        board = board_txt(game_id)
        html += '<code><PRE>' + board.replace('\n', '<br/>') + '</PRE></code>'
        if session:
            if game_record[3]:
                # Game is started.
                if request.method == 'POST':
                    if session['uid'] == player_turn(game_id):
                        # Process submitted move.
                        move = request.form['move']
                        if is_valid_move_syntax(move):
                            if submit_move(move, game_id):
                                return redirect(url_for('chess'))
                            else:
                                html += '<p><font color=red>Invalid move.</font></p>'
                        else:
                            html += '<p><font color=red>Invalid move syntax.</font></p>'
                    else:
                        html += "<p>It's not your turn.</p>"
            else:
                html += '<p>This game has not started yet.</p>'
                if session['uid'] == player2:
                    html += '<p><a href=/chess/accept/' + game_id + '>Accept</a></p>'
        else:
            if game_record[4]:
                pass # Is public game
            else:
                html += '<p>You do not have access to this game.</p>'
    else:
        html += '<p>Game does not exist.</p>'
    html = fill_page(html)
    return render_template_string(html, game_id=game_id, player1=player1, player2=player2, board=board)

@app.route('/chess/accept/<game_id>', methods=['POST', 'GET'])
def chess_accept(game_id):
    if session:
        game_record = sql_query('SELECT * FROM chessGames WHERE id=?', game_id)[0]
        if game_record[2] == session['uid']:
            sql_execute('UPDATE chessGames SET start=1 WHERE id=?', game_id)
            return redirect(url_for('chess'))
        else:
            return redirect(url_for('chess'))