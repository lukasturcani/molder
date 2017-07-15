#!/home/lukas/anaconda3/bin/python3.6

import cgi
import json

form = cgi.FieldStorage()

print('Content-Type: text/plain\n')

with open('database.json', 'r') as f:
    db = json.load(f)
    # print('hi', form.getfirst('username'))
    print(json.dumps(([form.getfirst('username')], list(db.items())[0])))
