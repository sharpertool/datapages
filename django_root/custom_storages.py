from django.conf import settings
from django.contrib.staticfiles.storage import CachedFilesMixin, ManifestFilesMixin
from pipeline.storage import PipelineMixin
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(PipelineMixin, ManifestFilesMixin, S3Boto3Storage):
    """ Custom Static Storage class, specify a unique directory """
    location = getattr(settings, 'STATICFILES_LOCATION', None)

class MediaStorage(S3Boto3Storage):
    """ Custom Media Storage class, specify a unique directory """
    location = settings.MEDIAFILES_LOCATION

