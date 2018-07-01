import datetime

class Config(object):
    PERMANENT_SESSION_LIFETIME=datetime.timedelta(minutes=60)
    REMEMBER_COOKIE_DURATION=datetime.timedelta(minutes=60)

class DevelopmentConfig(Config):
    FLASK_DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI="sqlite:///db/helix.sqlite"

class ProductionConfig(Config):
    FLASK_DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI="sqlite:///db/helix.sqlite"

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
