from .base import *
import os

from dotenv import load_dotenv
from ..logging import *
load_dotenv(Path.joinpath(BASE_DIR,'.env'))

SECRET_KEY = os.environ.get('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST':'db',
        'PORT':'3306',
        'USER':'admin',
        'PASSWORD':'admin',
        'NAME': 'dentistore'
    }
}

STATIC_ROOT = Path.joinpath(BASE_DIR,'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'