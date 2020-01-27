from app import app
from markdown import markdown
from flask import render_template_string
from app.blog_helpers import render_markdown

# generic page
@app.route("/<view_name>")

# render generic page
def render_page(view_name):
    html = render_markdown(view_name + '.md')
    return render_template_string(html, view_name = view_name)