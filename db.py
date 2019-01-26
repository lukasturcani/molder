import sqlite3
import os
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
    return g.db


def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():

    current_app.teardown_appcontext(close_db)

    if os.path.exists(current_app.config['DATABASE']):
        return

    cmd = '''
        CREATE TABLE results (
            username TEXT,
            molecule TEXT,
            opinion TEXT,
            history_index INTEGER,
            PRIMARY KEY (username, molecule)
        )
    '''

    db = get_db()
    db.execute(cmd)
    db.commit()
