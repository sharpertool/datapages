import environ

env = environ.Env()
from os.path import join

from .common import *

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
    'webpack_loader'
]

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

INTERNAL_IPS = ('127.0.0.1', '10.0.2.2',)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 8026
EMAIL_HOST = 'localhost'


WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': env.str('BUNDLE_DIR_NAME', default='js/'),
        'STATS_FILE': join(CLIENT_DIR, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': ['.+\.hot-update.js', '.+\.map']
    }
}
