import logging
import os
from flask import Flask

app = Flask(__name__)

def create_app(test_config=None):
    # create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'WASPGpt.sqlite')
    )

    if test_config is None:
        # loads the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # loads the instance config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import db
    db.fill_app(app)

    from . import db
    db.test_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import sites
    app.register_blueprint(sites.bp)
    app.add_url_rule('/', endpoint='index')

    return app

if __name__ == "__main__":
    logging.info("Starting app.")
    app.run(host="0.0.0.0", port=8000)