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


def next_molecule(username, num_seen):
    """
    Returns the next molecule to be judged by the user.

    Parameters
    ----------
    username : :class:`str`
        The username of the person sending the request.

    num_seen : :class:`int`
        The number of molecules the user has seen previously.

    Returns
    -------
    :class:`tuple` of :class:`str`
        The first string is InChI of the next molecule the client will
        render. The second string is the structural info of the
        molecule.

    """

    with open('database.json', 'r') as f:
        db = json.load(f)

    # If all of the shared molecules have been evaluated, try loading
    # the user-specific molecules.
    if len(db.keys()) >= num_seen:
        num_seen -= len(db.keys())

        with open(username+'.json', 'r') as f:
            db = json.load(f)
            

    # Go through the database in order.
    return sorted(db.items())[num_seen]


form = cgi.FieldStorage()
username = form.getfirst('username')
history = json.loads(form.getfirst('history'))
molecule = form.getfirst('molecule')
opinion = int(form.getfirst('opinion'))

update_history(username, history)
update_opinions(username, molecule, opinion)
print(json.dumps(next_molecule(username, len(history))))
