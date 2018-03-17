# This file is exec'd from settings.py, so it has access to and can
# modify all the variables in settings.py.

# If this file is changed in development, the development server will
# have to be manually restarted because changes will not be noticed
# immediately.

import environ
import sys

print(f"Loaded local_config from {__file__}.")

env = environ.Env()


if len(sys.argv) > 1 and sys.argv[1] == 'test':
    print("Running test mode..")
    from datapages.settings.test import *
else:
    if env.bool('DJANGO_DOCKER', False):
        env.read_env('.env.local.docker')
    else:
        env.read_env('.env.local')

    from datapages.settings.dev import *

###################
# DEPLOY SETTINGS #
###################

# Domains for public site
ALLOWED_HOSTS = [
    "127.0.0.1",
    "0.0.0.0",
    "localhost",
    "datapages.local",
    "datapages.io",
]

INTERNAL_IPS = ('127.0.0.1',
                'localhost',
                'datapages.local',
                '0.0.0.0:8001',)

