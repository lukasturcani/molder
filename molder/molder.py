from flask import Blueprint, current_app
import json
from db import get_db

bp = Blueprint('molder', __name__)


@bp.route('/mol/<molecule>', methods=('GET', ))
def get_molecule(molecule):
    """
    Returns the structural info of `molecule`.

    Parameters
    ----------
    molecule : :class:`str`
        The InChI of a molecule which the client wants the structure
        of.

    Returns
    -------
    :class:`str`
        The structure of the molecule in the form of a MDL V3000
        ``.mol`` file.

    """

    return current_app.mols[molecule]


#!/home/lukas/anaconda3/bin/python3.6
"""
Sends user their previous history and first molecule of the session.

"""

import cgi
import json
import os


if __name__ == '__main__':
    # Import "next_molecule" from next_mol.cgi.
    gvars = {}
    with open('next_mol.cgi', 'r') as f:
        exec(f.read(), gvars)
    next_molecule = gvars['next_molecule']

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

    print('Content-Type: text/plain\n')
    print(json.dumps((history, next_mol)))


#!/home/lukas/anaconda3/bin/python3.6
"""
Saves data from client and sends back the next molecule.

If a different algorithm for selecting the next molecule is to be used
:func:`next_molecule` will need to be changed. The only requirement is
that it returns a tuple consisting of two strings. The first string is
the InChI of the next molecule and the second string is the structure
of the next molecule (V3000 .mol file format). Arguments can be changed
as necessary for the chosen algo.

"""


@bp.route('/opinions/<username>/<molecule>/<opinion>',
          methods=('POST', ))
def update_opinion(username, molecule, opinion):
    """
    Updates the results database with the users opinion.

    Parameters
    ----------
    username : :class:`str`
        The username of the person sending the request.

    molecule : :class:`str`
        The InChI of the molecule about which the user is sending their
        opinion.

    opinion : :class:`str`
        The user's opinion about `molecule`.

    Returns
    -------
    None : :class:`NoneType`

    """

    db = get_db()

    history_query = '''
        SELECT MAX(history_index)
        FROM results
        WHERE
           username = ?
    '''
    history_index = db.execute(history_query, (username, )).fetchone()
    history_index += 1

    db.execute('INSERT INTO results VALUES (?, ?, ?, ?)',
               (username, molecule, opinion, history_index))


def next_molecule(username):
    """
    Returns the next molecule to be judged by the user.

    Parameters
    ----------
    username : :class:`str`
        The username of the person sending the request.

    Returns
    -------
    :class:`tuple` of :class:`str`
        The first string is InChI of the next molecule the client will
        render. The second string is the structural info of the
        molecule.

    """

    # Load the set of shared molecules that every user sees.
    with open('shared.json', 'r') as f:
        shared = set(json.load(f))

    # Make a set of all molecules judged by all users. This will
    # ensure that each user looks at unique molecules.
    seen = set()
    for path in iglob('*/history.json'):
        with open(path, 'r') as f:
            history = json.load(f)
            # If looking at the molecules judges by other users, ignore
            # the fact that they've already looked at shared molecules.
            if username not in path:
                history = (mol for mol in history if mol not in shared)
            seen.update(history)

    # Load molecules in the database, excluding the ones already seen.
    with open('database.json', 'r') as f:
        db = json.load(f)
        db = {key: value for key, value in db.items() if
              key not in seen}

    # Pick the next molecule at random from the available ones.
    chosen_key = np.random.choice(list(db.keys()))
    # Go through the database in order.
    return chosen_key, db[chosen_key]


if __name__ == '__main__':
    form = cgi.FieldStorage()
    username = form.getfirst('username')
    history = json.loads(form.getfirst('history'))
    molecule = form.getfirst('molecule')
    opinion = int(form.getfirst('opinion'))

    update_history(username, history)
    update_opinions(username, molecule, opinion)

    print('Content-Type: text/plain\n')
    print(json.dumps(next_molecule(username)))
