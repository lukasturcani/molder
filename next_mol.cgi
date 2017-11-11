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


import cgi
from os.path import join
import json
import numpy as np
from glob import iglob


print('Content-Type: text/plain\n')


def update_history(username, history):
    """
    Writes `history` to the user's ``history.json`` file.

    Parameters
    ----------
    username : :class:`str`
        The username of the person sending the request.

    history : :class:`list` of :class:`str`
        A list holding the InChI's of molecules previously seen by
        the user.

    Returns
    -------
    None : :class:`NoneType`

    """

    with open(join(username, 'history.json'), 'w') as f:
        json.dump(history, f)


def update_opinions(username, molecule, opinion):
    """
    Updates the user's ``opinions.json`` file.

    Parameters
    ----------
    username : :class:`str`
        The username of the person sending the request.

    molecule : :class:`str`
        The InChI of the molecule about which the user is sending their
        opinion.

    opinion : :class:`int`
        The user's opinion about `molecule`. The number corresponds to
        a button pressed on the website.

    Returns
    -------
    None : :class:`NoneType`

    """

    with open(join(username, 'opinions.json'), 'r') as f:
        opinions = json.load(f)

    opinions[molecule] = opinion
    with open(join(username, 'opinions.json'), 'w') as f:
        json.dump(opinions, f)


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


form = cgi.FieldStorage()
username = form.getfirst('username')
history = json.loads(form.getfirst('history'))
molecule = form.getfirst('molecule')
opinion = int(form.getfirst('opinion'))

update_history(username, history)
update_opinions(username, molecule, opinion)
print(json.dumps(next_molecule(username)))
