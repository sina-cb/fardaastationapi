import logging
import sqlalchemy

import episodes
from episodes import Episodes
from time import time
from logging import error as logi
from flask import Flask, jsonify


def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    # Setup the data model.
    with app.app_context():
        model = episodes
        model.init_app(app)

    @app.route('/')
    def welcome_screen():
        episodes = {'timestamp': int(time())}

        logi("Trying to run")
        try:
            episodes = Episodes.query.all()
        except sqlalchemy.exc.OperationalError, e:
            logi("OperationalError: {}".format(e))
        except KeyError, e:
            logi("KeyError: {}".format(e))
        except:
            import sys
            logi("Something unexpected happened: ")
            logi(sys.exc_info()[0])

        logi(episodes)

        return jsonify(episodes)

    # Add an error handler. This is useful for debugging the live application,
    # however, you should disable the output of the exception for production
    # applications.
    @app.errorhandler(500)
    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    return app
