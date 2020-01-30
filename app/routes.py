from app import app
from markdown import markdown
from flask import render_template_string, request, session, redirect, url_for, escape
from app.blog_helpers import render_markdown, render_html
import os, sqlite3, secrets, hashlib

app.secret_key = '`(7h_B/G PH:=IyT-$L^mE~5AR!Y|?/;i=2z1]ESGMKRtg-f'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get user record from SQLite database user.db
        conn = sqlite3.connect('user.db')
        udata = conn.cursor().execute('SELECT * FROM users WHERE name=?', (request.form['username'],)).fetchall()

        # Check that 1 matching record was found AND check hash from db against hash of salt + provided password
        if len(udata) == 1 and udata[0][3] == hashlib.sha256((udata[0][2] + request.form['password']).encode()).hexdigest():
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return render_html('login.html') + '\n<p><font color="red">invalid credentials</font></p>'

    return render_html('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_page('index')
    
# generic page
@app.route("/<view_name>")
def render_page(view_name):
    html = render_markdown(view_name + '.md')
    if session:
        html += 'logged in as: ' + session['username']
    return render_template_string(html, view_name = view_name)