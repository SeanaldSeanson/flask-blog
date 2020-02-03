from app import app
from markdown import markdown
from flask import render_template_string, request, session, redirect, url_for, escape, abort
from app.blog_helpers import render_markdown, read_txt, write_txt, backup_page, sql_execute, is_admin, is_view
import os, sqlite3, secrets, hashlib

app.secret_key = '`(7h_B/G PH:=IyT-$L^mE~5AR!Y|?/;i=2z1]ESGMKRtg-f'

# if __name__ == '__main__':
#     app.run(ssl_context='adhoc')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get user record from SQLite database user.db
        udata = sql_execute('SELECT * FROM users WHERE name=?', request.form['username'])

        # Check that 1 matching record was found AND check hash from db against hash of salt + provided password
        if len(udata) == 1 and udata[0][3] == hashlib.sha256((udata[0][2] + request.form['password']).encode()).hexdigest():
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return render_page('login', foot='\n<p><font color="red">invalid credentials</font></p>')

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
def render_page(view_name, head = read_txt('bar.html'), foot = ''):
    html = head
    if is_view(view_name + '.html'):
        html += '\n' + read_txt(view_name + '.html')
    else:
        abort(404)
    html += '\n' + foot
    login = 'Not logged in.'
    if session:
        login = 'Logged in as: ' + session['username']
    return render_template_string(html, view_name = view_name, login = login)

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