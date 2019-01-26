"""

"""

from flask import Flask
import os
import json
import molder
import db


def create_app(instance_path=None, test_config=None):
    """
    Create and configure the molder Flask application.

    Parameters
    ----------
    instance_path : :class:`str`, optional
        Path to the instance directory of the application.

    test_config : :class:`dict`, optional
        App config parameters used during testing.

    Returns
    -------
    :class:`flask.Flask`
        The application object.

    """

    app = Flask(__name__,
                instance_path=instance_path,
                instance_relative_config=True)

    if test_config is None:
        # Load the instance config, if it exists, when not testing.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config passed in.
        app.config.update(test_config)

    # Ensure the instance folder exists.
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    # Load database.json and shared.json into memory.
    with app.open_resource('database/database.json', 'rt') as f:
        app.mols = json.load(f)
    with app.open_resource('database/shared.json', 'rt') as f:
        app.shared_mols = set(json.load(f))

    # Create the database if it does not yet exist.
    db_path = os.path.join(app.instance_path, 'results.sql')
    if not os.path.exists(db_path):
        db.init_database(db_path)

    # Apply the molder blueprint to the app.
    app.register_blueprint(molder.bp)

    # Add database hooks to app.
    db.init_app(app)

    return app
