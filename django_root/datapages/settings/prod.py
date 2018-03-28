import environ

env = environ.Env()
from os.path import join

from .common import *

STATIC_ROOT = BASE_DIR('collectedstatic')

