from flask import Blueprint, current_app
import json
from db import get_db
import numpy as np

bp = Blueprint('molder', __name__)


def max_history_index(username):
    """
    Returns the maximum history index of a user.

    Parameters
    ----------
    username : :class:`str`
        The name of a user whose history index is needed.

    Returns
    -------
    :class:`int`
        The maximum history index of a user.

    """

    history_query = '''
        SELECT MAX(history_index)
        FROM results
        WHERE
           username = ?
    '''

    return get_db().execute(history_query, (username, )).fetchone()


@bp.route('/mols/<username>/<int:history_index>', methods=('GET', ))
def get_historical_molecule(username, history_index):
    """
    Returns the structural info of a molecule from the user's history.

    Parameters
    ----------
    username : :class:`str`, optional
        The username of the user.

    history_index : :class:`int`
        The history index of the molecule for that user.

    Returns
    -------
    :class:`str`
        A JSON array holding the InChI of the molecule and its
        structure, respectively.

    """

    query = '''
        SELECT molecule
        FROM results
        WHERE
            username = ? AND
            history_index = ?
    '''

    mol = get_db().execute(query, username, history_index).fetchone()
    return json.dumps([mol, current_app.mols[mol]])


@bp.route('/history_indices/<username>', methods=('GET', ))
def get_history_index(username):
    """
    Get the maximum history index for a user.

    Parameters
    ----------
    username : :class:`str`
        The username of the user whose history index is needed.

    Returns
    -------
    :class:`int`
        The user's maximum history index.

    """

    return max_history_index(username)


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

    h_index = max_history_index(username) + 1
    db = get_db()
    db.execute('INSERT INTO results VALUES (?, ?, ?, ?)',
               (username, molecule, opinion, h_index))
    db.commit()


@bp.route('/mols/<username>/next', methods=('GET', ))
def next_molecule(username):
    """
    Returns the next molecule to be judged by the user.

    Parameters
    ----------
    username : :class:`str`
        The username of the person sending the request.

    Returns
    -------
    :class:`str`
        A JSON array holding the InChI and structure of the next
        molecule, respectively.

    """

    db = get_db()

    # Make a set of all molecules judged by all users. This will
    # ensure that each user looks at unique molecules. Make sure
    # to exclude shared molecules which are to be seen by all users.
    seen_query = 'SELECT molecule FROM results'
    seen = {mol for mol, in db.execute(seen_query)
            if mol not in current_app.shared_mols}

    # Add any shared molecules that the user has already seen.
    seen_query = 'SELECT molecule FROM results WHERE username = ?'
    seen += {mol for mol, in db.execute(seen_query, (username, ))}

    # Get available molecules.
    db = {mol for mol in current_app.mols if mol not in seen}

    # Pick the next molecule at random from the available ones.
    molecule = np.random.choice(list(db.keys()))
    return json.dumps([molecule, current_app.mols[molecule]])
