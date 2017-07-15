#!/home/lukas/anaconda3/bin/python3.6
"""
Sends user their previous history and first molecule of the session.

"""

import cgi
import json
import os

print('Content-Type: text/plain\n')

form = cgi.FieldStorage()
username = form.getfirst('username')

with open('database.json', 'r') as f:
    db = json.load(f)

# If the user already used the app.
if os.path.exists(username):
    with open(os.path.join(username, 'history.json'), 'r') as f:
        history = json.load(f)

    num_seen = len(history)
    next_mol = sorted(db.items())[num_seen]

# If this is a new user.
else:
    history = []
    next_mol = sorted(db.items())[0]
    os.mkdir(username)
    with open(os.path.join(username, 'history.json'), 'w') as f:
        json.dump(history, f)
    with open(os.path.join(username, 'opinions.json'), 'w') as f:
        json.dump({}, f)

print(json.dumps((history, next_mol)))
