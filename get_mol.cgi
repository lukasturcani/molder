#!/usr/bin/python2.7
"""
Returns the structural info of a molecule to the client.

"""

import cgi
import json

print 'Content-Type: text/plain\n'


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
    :class:`tuple` of :class:`str`
        The first string is the InChI of the molecule, same as
        `molecule`, the second string is the structure of the molecule
        in the form of a MDL V3000 .mol file.

    """

    with open('database.json', 'r') as f:
        db = json.load(f)

    return molecule, db[molecule]


form = cgi.FieldStorage()
molecule = form.getfirst('molecule')
print json.dumps(get_molecule(molecule))
