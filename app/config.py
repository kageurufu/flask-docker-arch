import os


class BaseConfig:
    SECRET_KEY = os.urandom(32)

    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    DEBUG = True

    def __init__(self):
        for key in dir(self):
            if not key.startswith("_"):
                if key in os.environ:
                    value = str(os.environ.get(key))

                    if value in ('True', 'False'):
                        value = True if value == 'True' else False

                    elif value.isdigit():
                        value = int(value)

                    setattr(self, key, value)
        if 'SERVER_NAME' in os.environ:
            setattr(self, 'SERVER_NAME', os.environ.get('SERVER_NAME'))


class DebugConfig(BaseConfig):
    SQLALCHEMY_RECORD_QUERIES = True


class ProductionConfig(BaseConfig):
    DEBUG = False


def get_config():
    if os.environ.get('ENVIRONMENT', 'TESTING') == 'PRODUCTION':
        Config = ProductionConfig
    else:
        Config = DebugConfig
    return Config()
