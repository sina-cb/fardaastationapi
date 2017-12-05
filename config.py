import os

SECRET_KEY = 'secret'

DATA_BACKEND = 'cloudsql'
PROJECT_ID = 'fardaastationapi'

CLOUDSQL_USER = 'root'
CLOUDSQL_PASSWORD = ''
CLOUDSQL_DATABASE = 'fardaastation'

CLOUDSQL_CONNECTION_NAME = 'fardastationapi:us-east1:fardaastationapi-db'

LOCAL_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@127.0.0.1:3306/{database}').format(
    user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
    database=CLOUDSQL_DATABASE)

LIVE_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@localhost/{database}'
    '?unix_socket=/cloudsql/{connection_name}').format(
    user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
    database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)

if os.environ.get('GAE_INSTANCE'):
    SQLALCHEMY_DATABASE_URI = LIVE_SQLALCHEMY_DATABASE_URI
else:
    SQLALCHEMY_DATABASE_URI = LOCAL_SQLALCHEMY_DATABASE_URI

GOOGLE_OAUTH2_CLIENT_ID = \
    ''

GOOGLE_OAUTH2_CLIENT_SECRET = ''