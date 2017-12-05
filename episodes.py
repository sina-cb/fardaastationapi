import peewee
import os
import config
from peewee import *

db = None
if (os.getenv('SERVER_SOFTWARE') and
        os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
    db = MySQLDatabase(config.CLOUDSQL_DATABASE, unix_socket='/cloudsql/{}'.format(config.CLOUDSQL_CONNECTION_NAME),
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


def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    Episodes.create_table()
    print("All tables created")


if __name__ == '__main__':
    _create_database()
