import logging

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

    @app.route('/')
    def welcome_screen():
        episodes = {'timestamp': int(time())}

        logi("Trying to run")
        # q = Episodes.insert(timestamp = 123, title = "SINA", date = "123",
        #                     base_uri = "www.sina.com", low_quality = "123",
        #                     high_quality = "High", image_uri = "Image")
        # q.execute()
        title = ''
        for episode in Episodes.filter(timestamp = 123):
            title = episode.title
        logi("HERE")

        return '<h1>Episode title: {}</h1>'.format(title)

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
