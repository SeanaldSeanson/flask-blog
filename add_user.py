import sqlite3, secrets, hashlib, sys

args = sys.argv
args.pop(0)

helptxt = 'Usage:\nadd_user.py USERNAME PASSWORD [ADMIN]\nADMIN = 0 or 1, default 0'

if len(args) != 2:
    if len(args) == 3:
        if args[2] != '0' and args[2] != '1':
            print(helptxt)
            exit(1)
        admin = args[2]
    else:
        print(helptxt)
        exit(1)
else:
    admin = 0

uname = args[0]
passwd = args[1]

newSalt = secrets.token_hex(16)
newHash = hashlib.sha256((newSalt + passwd).encode()).hexdigest()

conn = sqlite3.connect('blog.db')
c = conn.cursor()

try:
    c.execute('INSERT INTO users (name, salt, hash, admin) VALUES (?,?,?,?)', (uname, newSalt, newHash, admin))
except sqlite3.IntegrityError as e:
    print('Invalid database input: ' + str(e))

conn.close()
exit(0)