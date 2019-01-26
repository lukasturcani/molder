import sqlite3
import os
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_app(app):

    app.teardown_appcontext(close_db)

    if os.path.exists(app.config['DATABASE']):
        return

    cmd = '''
        CREATE TABLE results (
            username TEXT,
            molecule TEXT,
            opinion TEXT,
            history_index INTEGER,
            PRIMARY KEY (username, molecule),
            UNIQUE (username, history_index)
        )
    '''

    db = sqlite3.connect(app.config['DATABASE'])
    db.execute(cmd)
    db.commit()
