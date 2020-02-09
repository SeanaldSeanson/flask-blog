from app import app
from markdown import markdown
from flask import render_template_string, request, session, redirect, url_for, escape, abort, send_from_directory, send_file
from app.blog_helpers import render_markdown, read_txt, write_txt, backup_page, is_admin, is_view, fill_page, login_text, sql_query, sql_execute
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
        udata = sql_query('SELECT * FROM users WHERE name=?', (request.form['username'],))

        # Check that 1 matching record was found AND check hash from db against hash of salt + provided password
        if len(udata) == 1 and udata[0][3] == hashlib.sha256((udata[0][2] + request.form['password']).encode()).hexdigest():
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return render_page('login', foot='<p>Invalid Credentials</p>')

    return render_page('login')

@app.route('/logout')
def logout():
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
    if session and is_admin(session['username']):
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
        html += '<p>' + PurePath(p).stem + '</p>\n'
    html = fill_page(html)
    return render_template_string(html, view_name = 'all', login = login_text())

@app.route('/chess')
def chess():
    html = read_txt('chess.html')
    html = fill_page(html)
    active = ''
    pending = ''
    if session:

        html += '<p><a href=/chess/new>Start Game</a></p>'

        html += '<h2>Active Games</h2>{{active}}'
        active_games = sql_query('SELECT * FROM chessGames WHERE (player1=? OR player2=?) AND start=1', (session['username'], session['username']))

        if len(active_games) > 0:
            for g in active_games:
                active += '<p>' + g[0] + ': ' + g[1] + ' v. ' + g[2] + '</p>'
        else:
            active = 'No active games.'
        
        html += '<h2>Pending Games</h2>{{pending}}'
        pending_games = sql_query('SELECT * FROM chessGames WHERE (player1=? OR player2=?) AND start=0', (session['username'], session['username']))
        if len(pending_games) > 0:
            for g in pending_games:
                accept_link = '<a href=/games/' + str(g[0]) + '/accept' + '>accept</a>'
                pending += str(g[0]) + ': ' + g[1] + ' v. ' + g[2] + accept_link
        else:
            pending = 'No pending games.'
    else:
        html += '<p>You must log in to play chess.</p>'
    
    return render_template_string(html, view_name='chess', login = login_text(), active=active, pending=pending)

@app.route('/chess/new', methods=['GET', 'POST'])
def chess_new():
    if session:
        if request.method == 'POST':
            if len(sql_query('SELECT name FROM users WHERE name=?', (request.form['player'],))) == 1:
                sql_execute('INSERT INTO chessGames (player1, player2, start) VALUES(?,?,0)', session['username'], request.form['player'])
            return redirect(url_for('chess'))
        else:
            return render_page('chess_new')
    else:
        abort(403)

@app.route('/chess/<game>')
def chess_game():
    pass


# @app.route('/games')
# def game_list():
    # return ''
# 
# @app.route('/games/<path:path>')
# def send_game_file(path):
    # return send_from_directory('../games', path, as_attachment=False)
    # with open('games/' + path) as file:
        # return file.read()