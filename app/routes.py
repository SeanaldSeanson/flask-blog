from app import app
from markdown import markdown
from flask import render_template_string, request, session, redirect, url_for, escape, abort
from app.blog_helpers import render_markdown, read_txt, sql_execute, is_admin, is_view
import os, sqlite3, secrets, hashlib

# What happens if this is generated randomly here?
app.secret_key = '`(7h_B/G PH:=IyT-$L^mE~5AR!Y|?/;i=2z1]ESGMKRtg-f'


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
            return read_txt('login.html') + '\n<p><font color="red">invalid credentials</font></p>'

    return render_page('login')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/')
@app.route('/index')
def index():
    return render_page('index')

@app.route('/blog/<view_name>')
def render_blog(view_name):
    render_page('blog/view_name')

# generic page
@app.route('/<view_name>')
def render_page(view_name = '', head = read_txt('bar.html'), foot = ''):
    html = head
    if is_view(view_name + '.md'):
        print('load: ' + view_name + '.md')
        html += '\n' + render_markdown(view_name + '.md')
    elif is_view(view_name + '.html'):
        print('load: ' + view_name + '.html')
        html += '\n' + read_txt(view_name + '.html')
    else:
        abort(404)
    html += '\n' + foot
    login = 'Not logged in.'
    if session:
        login = 'Logged in as: ' + session['username']
    return render_template_string(html, view_name = view_name, login = login)

# edit generic page
@app.route('/edit/<view_name>')
def edit_page(view_name):
    if session and is_admin(session['username']):
        html = render_page('edit')
        if os.path.isfile(view_name + '.md'):
            view_name += '.md'
        elif os.path.isfile(view_name + '.html'):
            view_name += '.html'
        else:
            view_name = ''
        page = read_txt(view_name)
        return render_template_string(html, view_name = view_name, page = page)