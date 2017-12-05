from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Episodes(db.Model):
    timestamp = db.Column('timestamp', db.BigInteger)
    title = db.column('title', db.Unicode)
    date = db.column('date', db.Unicode)
    base_uri = db.Column('base_uri', db.String, primary_key=True)
    low_quality = db.Column('low_quality', db.String)
    high_quality = db.Column('high_quality', db.String)
    image_uri = db.Column('image_uri', db.String)

    def __init__(self, timestamp, title, date, base_uri, low_quality, high_quality, image_uri):
        self.timestamp = timestamp
        self.title = title
        self.date = date
        self.base_uri = base_uri
        self.low_quality = low_quality
        self.high_quality = high_quality
        self.image_uri = image_uri


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)


def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('./config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()
