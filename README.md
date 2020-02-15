# Flask website for CS 232
A basic Flask website, plus multiplayer chess.

# Design
## Overview
The main pages are stored in app/views and are each modified if necessary by a corresponding function in routes.py.
The app/views/parts directory stores html documents which are meant to be used as components of other pages, or that are not associated with one particular route.

blog_helpers.py includes helper functions for common operations including querying and modifying the 'blog.db' sqlite3 database, reading and writing text files, and generating or modifying page content.

chess_helpers.py includes helper functions for the (not currently fully working) multiplayer chess feature of the site.

## Pages
Most pages use the 'fill_page' function from blog_helpers.py to prepend the content of bar.html, which defines a navigation bar to shown at the top of each page.

### /all
For /all, the 'all' function reads all.html and populates a list of links to pages by searching for any html files in app/views/.

### /<page_name>
For pages in app/views/ that do not have their own specified functions in routes.py, the 'render_page' function is used by default to load the html page if it exists, prepend the standard navigation bar, and return the page to the user. If their is no html document is app/views/, a 404 error will sent instead.

### /edit/<page_name>
If the user is currently logged in as a user with administrative priveleges, this route will allow the user to edit the page specified by page_name. The page will be backed up with a .bak extension added to the original file name.

### /chess
This is the main page for the site's (not yet fully working) multiplayer chess system, which lists all in-progress and pending games for the currently logged in user, allowing the user to accept challenges issued by other players or choose an ongoing game to view.

### /chess/<game_id>
This route will load the chess game specified by game_id, an integer identifier.

### /chess/accept/<game_id>
This route will allow a user to accept an invitation to a chess match, marking the game as started in the database.

### /chess/new
This route will allow a user to issue a challenge to another user, adding a pending game to the database.

## Authentication
user data is stored in the sqlite3 database file blog.db, in the 'users' table, with fields id (INTEGER), name (TEXT), salt (TEXT), hash (TEXT), and admin (INTEGER).
id and name are both unique primary keys, to enforce unique usernames for logins but allowing for the potential to change a user's username. id autoincrements and does not need to be specified when adding a user.
salt contains a random hexadecimal number that is prepended to the user's password to produce a the string from which the user's hash is derived, allowing two users to use the same password but still have different hashes. The hash field stores the SHA256 hash produced from this process.
Currently, new users cannot be added through the website, but the script add_user.py is available to help with adding users to the database manually.