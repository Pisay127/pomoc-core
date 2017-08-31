import os

# Use ConfigParser in the future.

TOKEN_EXPIRES = 3600
APP_ENV = os.environ.get('APP_ENV') or 'local'
DB_OPTIONS = {
    "pool_recycle": 3600,
    "pool_size": 10,
    "pool_timeout": 30,
    "max_overflow": 30,
    "echo": True,  # Replace value with a variable in the future.
    "execution_options": {
        "autocommit": True  # Replace value with a variable in the future. You know, a variable from the settings.
    }
}

if APP_ENV == 'dev' or APP_ENV == 'live':
    DB_CONFIG = ("username", "password", "host", "database")
    DB_URL = "postgresql+psycopg2://{0}:{1}@{2}/{3}".format(*DB_CONFIG)
else:
    DB_CONFIG = ("host", "database")
    DB_URL = "postgresql+psycopg2://{0}/{1}".format(*DB_CONFIG)