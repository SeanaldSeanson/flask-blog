from flask import session
from markdown import markdown
import os, sqlite3, secrets, hashlib

def render_markdown(file_name, dir_path = 'app/views'):
    return markdown(read_txt(file_name, dir_path))

def read_txt(file_name, dir_path = 'app/views'):
    txt = ''
    path = os.path.join(dir_path, file_name)
    with open(path) as txt_file:
        txt = txt_file.read()
    return txt

def write_txt(content, file_name, dir_path = 'app/views'):
    with open(os.path.join(dir_path, file_name), 'w') as txt_file:
        txt_file.write(content)

def backup_page(file_name, dir_path = 'app/views', backup_name = ''):
    if backup_name == '':
        backup_name = file_name + '.bak'
    with open(os.path.join(dir_path, file_name)) as old_file:
        with open(os.path.join(dir_path, backup_name), 'w') as backup:
            backup.write(old_file.read())

def sql_query(sql, *parameters):
    conn = sqlite3.connect('blog.db')
    query = conn.cursor().execute(sql, parameters).fetchall()
    conn.close()
    return query

def sql_execute(sql, *parameters):
    conn = sqlite3.connect('blog.db')
    conn.cursor().execute(sql, parameters)
    conn.commit()
    conn.close()

def is_admin(uid):
    if sql_query('SELECT admin FROM users WHERE id=?', uid)[0][0]:
        return True
    return False

def is_view(view_name = '', dir_path = 'app/views'):
    if os.path.isfile(os.path.join(dir_path, os.path.normpath(view_name))):
        return True
    return False

def fill_page(html, head = read_txt('bar.html', 'app/views/parts'), foot=''):
    html = head + '\n' + html + '\n' + foot
    return html

def login_text():
    if session:
        return 'Logged in as: ' + get_uname(session['uid'])
    return 'Not logged in.'

def add_user(name, password, admin=0):
    newSalt = secrets.token_hex(16)
    newHash = hashlib.sha256((newSalt + password).encode()).hexdigest()

    sql_execute('INSERT INTO users (name, salt, hash) VALUES (?,?,?)', name, newSalt, newHash)

def get_uname(uid):
    return sql_query('SELECT name FROM users WHERE id=?', uid)[0][0]

def get_uid(username):
    return sql_query('SELECT id FROM users WHERE name=?', username)[0][0]