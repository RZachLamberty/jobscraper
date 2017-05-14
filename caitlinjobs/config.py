import os

DEBUG = True

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    '\xa1\xd1\xcd\x9ep9[\x1e%7E\xfb\x81}\xc9d{\x1a\xe5Z\xa6\x89\xee{'
)

# you can override this here; it will be set automatically in run.py and
# __init__.py based on the fdbcred parameter (so we don't hardcode any of this)
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', None)
SQLALCHEMY_TRACK_MODIFICATIONS = False
