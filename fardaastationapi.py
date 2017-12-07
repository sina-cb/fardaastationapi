import logging

from episodes import find_updates, db
from logging import error as logi
from flask import Flask, jsonify, request


def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['JSON_AS_ASCII'] = False

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    @app.before_request
    def before_request():
        db.connect()

    @app.after_request
    def after_request(response):
        db.close()
        return response

    @app.route('/get_new_episodes')
    def get_new_episodes():
        appengine_request = request.headers.get('X-Appengine-Cron')
        if appengine_request == 'true':
            from scraper import update_episodes
            update_episodes()
            return '<h1>Success</h1>'
        else:
            return '<h1>This is a crobjob and all the requests should come from appengine.</h1>'

    @app.route('/get_updates')
    def get_update():
        timestamp = request.args.get('timestamp', '')

        if timestamp == '':
            logi('Default timestamp')
            timestamp = 0
        else:
            timestamp = long(timestamp)

        result = find_updates(timestamp)

        return jsonify(result)

    @app.route('/')
    def welcome():
        message = '{}{}{}'.format('<h1>Welcome to FardaStationAPI WebService</h1>',
                                  '<p>To get information about the latest episodes of Fardaa Station (by '
                                  'RadioFarda.com) please send a GET request to '
                                  'http://fardastationapi.appspot.com/get_updates URL.</p>',
                                  '<p>A UNIX epoch timestamp can also be passed in as an argument to filter out the '
                                  'episodes before that timestamp. Example: '
                                  'https://fardastationapi.appspot.com/get_updates?timestamp=1512629949</p>')
        return message

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
