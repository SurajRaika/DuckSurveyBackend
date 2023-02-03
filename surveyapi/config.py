class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///survey.db' # survey.db is file name of sqlite database file
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # used for encryption and session management
    SECRET_KEY = 'myssdaasdsdfaecdefdaasdasdtkey'