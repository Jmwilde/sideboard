import os


class Config(object):
    # Heroku / SQLAlchemy compatibility fix
    uri = os.getenv("DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = uri or \
        'postgresql://john:postgres@localhost/sideboarddb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = \
        'postgresql://john:postgres@localhost/sideboardtestdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
