from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    """ Custom Static Storage class, specify a unique directory """
    location = settings.STATICFILES_LOCATION

class MediaStorage(S3Boto3Storage):
    """ Custom Media Storage class, specify a unique directory """
    location = settings.MEDIAFILES_LOCATION

