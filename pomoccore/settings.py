# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

# Use ConfigParser in the future.

ACCESS_TOKEN_EXPIRES = 86400
REFRESH_TOKEN_EXPIRES = 259200
TOKEN_SECRET_LENGTH = 32
SERVER_SECRET = 'qqw#33A4dT4VnZ!m+7ewEQ2+JZk$T&8U2L&SQ+^J_h9$bQVX2*m$jMvWMUr@MGJj'  # Change this in production.
APP_ENV = 'dev'  # os.environ.get('APP_ENV') or 'local' Replace this with something from a ConfigParser
DB_OPTIONS = {
    'pool_recycle': 3600,
    'pool_size': 10,
    'pool_timeout': 30,
    'max_overflow': 30,
    'echo': True,  # Replace value with a variable in the future.
    'execution_options': {
        'autocommit': True  # Replace value with a variable in the future. You know, a variable from the settings.
    }
}

PASSWORD_SCHEMES = [
    'pbkdf2_sha256'
]

if APP_ENV == 'dev' or APP_ENV == 'live':
    DB_CONFIG = ('pomoccore_app', '!Pisay127PassesCMSC127!', 'localhost', 'pomoccore_db')
    DB_URL = 'postgresql+psycopg2://{0}:{1}@{2}/{3}'.format(*DB_CONFIG)
else:
    DB_CONFIG = ('localhost', 'pomoccore_db')
    DB_URL = 'postgresql+psycopg2://{0}/{1}'.format(*DB_CONFIG)