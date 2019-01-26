"""

"""

from flask import Flask
import os
import json
from molder import db, site


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
        # Load default config values.
        app.config.from_object('molder.default_settings')
        # Load the instance config, if it exists, when not testing.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config passed in.
        app.config.update(test_config)

    # Ensure the instance folder exists.
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    # Load database.json and shared.json into memory.
    with app.open_resource('database/database.json') as f:
        app.mols = json.loads(f.read().decode('ascii'))
    with app.open_resource('database/shared.json') as f:
        app.shared_mols = set(json.loads(f.read().decode('ascii')))

    # Create the database if it does not yet exist.
    db.init_app(app)

    # Apply the molder blueprint to the app.
    app.register_blueprint(site.bp)

    return app
