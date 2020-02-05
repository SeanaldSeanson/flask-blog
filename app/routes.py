from app import app
from markdown import markdown
from flask import render_template_string, request, session, redirect, url_for, escape, abort
from app.blog_helpers import render_markdown, read_txt, write_txt, backup_page, sql_execute, is_admin, is_view, fill_page, login_text
from glob import glob
from pathlib import PurePath
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
    else:
        abort(404)
    return render_template_string(fill_page(html, head, foot), view_name = view_name, login = login_text())

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
    print(html)
    return render_template_string(html, view_name = 'all', login = login_text())