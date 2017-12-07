import peewee
import os
import config
from peewee import *
from logging import error as logi

db = None
if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
    cloudsql_unix_socket = os.path.join(
        '/cloudsql', config.CLOUDSQL_CONNECTION_NAME)

    db = MySQLDatabase(config.CLOUDSQL_DATABASE, unix_socket=cloudsql_unix_socket,
                       user=config.CLOUDSQL_USER, passwd=config.CLOUDSQL_PASSWORD)
else:
    db = MySQLDatabase(config.CLOUDSQL_DATABASE, user=config.CLOUDSQL_USER, passwd=config.CLOUDSQL_PASSWORD)


class Episodes(peewee.Model):
    timestamp = peewee.BigIntegerField()
    title = peewee.CharField()
    date = peewee.CharField()
    base_uri = peewee.CharField(primary_key=True)
    low_quality = peewee.CharField()
    high_quality = peewee.CharField()
    image_uri = peewee.CharField()

    class Meta:
        database = db


def find_updates(timestamp):
    results = []
    for episode in Episodes.select().where(Episodes.timestamp > timestamp):
        episode_map = {'timestamp': episode.timestamp,
                       'title': episode.title,
                       'date': episode.date,
                       'base_uri': episode.base_uri,
                       'low_quality': episode.low_quality,
                       'high_quality': episode.high_quality,
                       'image_uri': episode.image_uri}
        results.append(episode_map)

    return results


def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    try:
        Episodes.create_table()
    except:
        logi("Error happened.")

    print("All tables created")
