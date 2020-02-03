from markdown import markdown
import os, sqlite3

def render_markdown(file_name, dir_path = 'app/views'):
    return markdown(read_txt(file_name, dir_path))

def read_txt(file_name, dir_path = 'app/views'):
    txt = ''
    path = os.path.join(dir_path, file_name)
    with open(path) as txt_file:
        txt = txt_file.read()
    return txt

def sql_execute(sql, *parameters):
    return sqlite3.connect('blog.db').cursor().execute(sql, parameters).fetchall()

def is_admin(user):
    if sql_execute('SELECT admin FROM users WHERE name=?', user)[0][0]:
        return True
    return False

def is_view(view_name = '', dir_path = 'app/views'):
    print(view_name)
    print(os.path.join(dir_path, os.path.normpath(view_name)))
    if os.path.isfile(os.path.join(dir_path, os.path.normpath(view_name))):
        return True
    else:
        return False