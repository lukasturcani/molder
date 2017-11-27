#!/usr/bin/python2.7
"""
Sends user their previous history and first molecule of the session.

"""

import cgi
import json
import os
import logging

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logging.basicConfig(filename='log', filemode='w', level=1000)

    # Import "next_molecule" from next_mol.cgi.
    logger.debug('Importing "next_mol.cgi".')
    gvars = {}
    with open('next_mol.cgi', 'r') as f:
        exec f.read() in gvars
    next_molecule = gvars['next_molecule']

    logger.debug('Getting field storage.')
    form = cgi.FieldStorage()
    username = form.getfirst('username')

    logger.debug('Loading database.')
    with open('database.json', 'r') as f:
        db = json.load(f)

    # If the user already used the app.
    if os.path.exists(username):
        logger.debug('Loading previous history.')
        with open(os.path.join(username, 'history.json'), 'r') as f:
            history = json.load(f)
        next_mol = next_molecule(username)

    # If this is a new user.
    else:
        logger.debug('Setting up new user.')
        history = []
        os.mkdir(username)
        with open(os.path.join(username, 'history.json'), 'w') as f:
            json.dump(history, f)
        with open(os.path.join(username, 'opinions.json'), 'w') as f:
            json.dump({}, f)
        next_mol = next_molecule(username)

    print 'Content-Type: text/plain\n'
    print json.dumps((history, next_mol))
