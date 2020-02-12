# Flask website for CS 232
A basic Flask website, plus multiplayer chess maybe.

# Design

## Overview
The main pages are stored in app/views and are each modified if necessary by a corresponding function in routes.py.
The app/views/parts directory stores html documents which are meant to be used as components of other pages, or that are not associated with one particular route.

blog_helpers.py includes helper functions for common operations including querying and modifying the 'blog.db' sqlite3 database, reading and writing text files, and generating or modifying page content.

chess_helpers.py includes helper functions for the (not currently working) multiplayer chess feature of the site.

## Pages
Most pages use the 'fill_page' function from blog_helpers.py to prepend the content of bar.

## /all
For /all, the 'all' function reads all.html and populates a list of links to pages by searching for any html files in app/views/.

## /<page_name>

