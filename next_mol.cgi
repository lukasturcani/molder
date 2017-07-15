import cgi
from os.path import join
import json

print('Content-Type: text/plain\n')


def update_history(username, history):
    with open(join(username, 'history.json'), 'w') as f:
        json.dump(history, f)


def update_opinions(username, molecule, opinion):
    with open(join(username, 'opinions.json'), 'r') as f:
        opinions = json.load(f)

    opinions[molecule] = opinion
    with open(join(username, 'opinions.json'), 'w') as f:
        json.dump(opinions, f)


def next_molecule(username, num_seen):

    with open('database.json', 'r') as f:
        db = json.load(f)

    return sorted(db.items())[num_seen]


form = cgi.FieldStorage()
username = form.getfirst('username')
history = json.loads(form.getfirst('history'))
molecule = form.getfirst('molecule')
opinion = int(form.getfirst('opinion'))

update_history(username, history)
update_opinions(username, molecule, opinion)
print(next_molecule(username, len(history)))
