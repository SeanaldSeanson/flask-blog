from app import app

#home page
@app.route("/")
@app.route("/index")
def home():
    user = {'username': 'Sean'}
#    return "<h1>My Blog</h1>"
    return '''\
<html>
    <head>
        <title>Home Page - Blog</title>
    </head>
    <body>
        <h1>Hello, ''' + user['username'] + '''!</h1>
    </body>
</head>'''

@app.route("/about")
def about():
    return '''\
<html>
    <head>
        <title>About - Blog</title>
    </head>
    <body>
        <h1>All about me</h1>
        <p>Laboriosam est sed deleniti porro quis. Et nostrum minus distinctio quasi. Et delectus ipsum harum perspiciatis veniam nihil similique eos. Qui consequatur repellendus voluptas ad sunt. Velit enim culpa ea qui blanditiis corporis. Libero sapiente iste non dolorem.</p>
    </body>
</html>'''