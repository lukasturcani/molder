#!/usr/bin/python2.7
"""
Sends user their previous history and first molecule of the session.

"""

import cgi
import json
import os


if __name__ == '__main__':
    # Import "next_molecule" from next_mol.cgi.
    gvars, lvars = {}, {}
    with open('next_mol.cgi', 'r') as f:
        exec f.read() in gvars, lvars
    next_molecule = lvars['next_molecule']

    form = cgi.FieldStorage()
    username = form.getfirst('username')

    with open('database.json', 'r') as f:
        db = json.load(f)

    # If the user already used the app.
    if os.path.exists(username):
        with open(os.path.join(username, 'history.json'), 'r') as f:
            history = json.load(f)
        next_mol = next_molecule(username)

    # If this is a new user.
    else:
        history = []
        next_mol = next_molecule(username)
        os.mkdir(username)
        with open(os.path.join(username, 'history.json'), 'w') as f:
            json.dump(history, f)
        with open(os.path.join(username, 'opinions.json'), 'w') as f:
            json.dump({}, f)

    print 'Content-Type: text/plain\n'
    print json.dumps((history, next_mol))
