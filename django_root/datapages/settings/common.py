"""
Django settings for datapages project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import environ
import os

env = environ.Env()

DEBUG = env.bool('DJANGO_DEBUG', default=False)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
CONF_DIR = environ.Path(__file__)
PROJECT_DIR = environ.Path(__file__) - 3
BASE_DIR = PROJECT_DIR - 1

if DEBUG:
    print(f"Project Dir: {PROJECT_DIR} Bases dir: {BASE_DIR}")

SASS_PROCESSOR_ENABLED = DEBUG is True

# Make these unique, and don't share it with anybody.
SECRET_KEY = env.str('SECRET_KEY')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    'blog',
    'datasheet',
    'home',
    'search',
    'teconn',
    'panasonic',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    "wagtail.contrib.table_block",
    "wagtail.contrib.settings",

    'modelcluster',
    'taggit',

    #'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'pipeline',
    'raven.contrib.django.raven_compat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'datapages.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            PROJECT_DIR('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtail.contrib.settings.context_processors.settings'
            ],
        },
    },
]

WSGI_APPLICATION = 'datapages.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASE
DATABASES = {
    'default': env.db("DATABASE_URL", default='postgresql://datasheet_user:@localhost/datasheetai'),
}

DATABASES['default']['ATOMIC_REQUESTS'] = True

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Wagtail settings

WAGTAIL_SITE_NAME = env.str("WAGTAIL_SITE_NAME", default="datapages.io")

IFRAMELY_API_KEY = env.str('IFRAMELY_API_KEY', default=None)
WAGTAILEMBEDS_FINDERS = [
    {
        'class': 'wagtail.embeds.finders.oembed'
    },
]
if IFRAMELY_API_KEY:
    WAGTAILEMBEDS_FINDERS += [{
        'class': 'embed.finders.iframely',
        'key': IFRAMELY_API_KEY
    }]

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://{0}'.format(WAGTAIL_SITE_NAME)

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[WAGTAIL_SITE_NAME])

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
]



# Django Storages
AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID", default=None)
AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY", default=None)
AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME", default=None)
AWS_S3_REGION_NAME = env.str("AWS_S3_REGION_NAME", default="us-west-2")
AWS_S3_OBJECT_PARAMETERS = env.dict("AWS_S3_OBJECT_PARAMETERS",
                                    default={
                                        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
                                        'CacheControl': 'max-age=86400'
                                    })
AWS_S3_CUSTOM_DOMAIN = env.str("AWS_S3_CUSTOM_DOMAIN",
                               default="{}.s3.amazonaws.com".format(AWS_STORAGE_BUCKET_NAME))

STATIC_ROOT = PROJECT_DIR('static')
STATIC_URL = '/static/'


MEDIA_ROOT = PROJECT_DIR('media')
MEDIA_URL = '/media/'

SASS_PROCESSOR_INCLUDE_DIRS = [
    PROJECT_DIR('datapages/static/sass'),
    PROJECT_DIR('datasheet/static/sass'),
]
SASS_PROCESSOR_ROOT = PROJECT_DIR('static')


PIPELINE = {
    'PIPELINE_ENABLED': DEBUG is False,  # Compress if not debugging
    'PIPELINE_COLLECTOR_ENABLED': True,  # Always collect assets
    'COMPILERS': [
        'pipeline.compilers.sass.SASSCompiler',
    ],
    'STYLESHEETS': {
        'datasheet': {
            'source_filenames': (
                'datasheet/static/sass/index.scss',
            ),
            'output_filename': 'css/datasheet.css',
            'extra_context': {
                'media': 'screen,projection'
            }
        }
    },
    'JAVASCRIPT': {
        'datasheet': {
            'source_filenames': (

            ),
            'output_filename': 'js/datasheet.js',
        },
        # 'stats': {
        #     'source_filenames': (
        #       'js/jquery.js',
        #       'js/d3.js',
        #       'js/collections/*.js',
        #       'js/application.js',
        #     ),
        #     'output_filename': 'js/stats.js',
        # }
    }
}

# Make the AWS Configuration optional, for local development
if (AWS_STORAGE_BUCKET_NAME is None):
    print("Using Local Static and Media files")
else:
    print("Setting up to use S3 storage.")

    CDN_URL = env.str('CDN_URL',
                      default=f"http://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/")

    MEDIAFILES_LOCATION = env.str("MEDIAFILES_LOCATION", default="mediafiles")
    MEDIA_ROOT = "mediafiles"
    MEDIA_URL = "{0}{1}/".format(CDN_URL, MEDIA_ROOT)
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

    ADMIN_MEDIA_PREFIX = "{}admin/".format(CDN_URL)


    print("CDN Domain:{}".format(AWS_S3_CUSTOM_DOMAIN))

# Get settings from environment. These are required to be set.
RAVEN_CONFIG = {
    'dsn': env.str('DJANGO_SENTRY_DSN', default=''),
    # Public DSN is passed to Javascript since it is client side and could be compromised.
    'public_dsn': env.str('DJANGO_SENTRY_PUBLIC_DSN', default=''),
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    # 'release': raven.fetch_git_sha(GIT_ROOT),
    'release': env.str('DATAPAGES_VERSION', default='')
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'WARNING', # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

