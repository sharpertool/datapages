# This file is exec'd from settings.py, so it has access to and can
# modify all the variables in settings.py.

# If this file is changed in development, the development server will
# have to be manually restarted because changes will not be noticed
# immediately.

import environ
import os
import sys

print("Loaded local_config from {}.".format(__file__))

env = environ.Env()

if len(sys.argv) > 1 and sys.argv[1] == 'test':
    print("Running test mode..")
    from datasheet_ai.settings.testing import *
else:

    if env.bool('DJANGO_DOCKER', False):
        env.read_env('.env.local.docker')
    else:
        env.read_env('.env.local')
    from datasheet_ai.settings.dev import *

# Make these unique, and don't share it with anybody.
SECRET_KEY = "<make yourself a new key!!>"
NEVERCACHE_KEY = "<make yourself a new key here too!>"


###################
# DEPLOY SETTINGS #
###################

# Domains for public site
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "datasheet.localhost",
]

INTERNAL_IPS = ('127.0.0.1',
                'localhost',)

MAILCHIMP_USERNAME = ''
MAILCHIMP_API_KEY = ''
MAILCHIMP_LIST_ID = ''

ANYMAIL = {
    "MAILGUN_API_KEY": "",
    "MAILGUN_SENDER_DOMAIN": "",
}

EMAIL_BACKEND = "anymail.backends.mailgun.MailgunBackend" 

