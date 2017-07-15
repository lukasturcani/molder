#!/home/lukas/anaconda3/bin/python3.6

import cgi
from os.path import join
import json

print('Content-Type: text/plain\n')


def get_molecule(molecule):

    with open('database.json', 'r') as f:
        db = json.load(f)

    return molecule, db[molecule]


form = cgi.FieldStorage()
molecule = form.getfirst('molecule')
print(json.dumps(get_molecule(molecule)))
