from .base import *

SECRET_KEY = 'admin123'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST':'localhost',
        'PORT':'3306',
        'USER':'root',
        'PASSWORD':'admin',
        'NAME': 'dentistore'
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'HOST':'db',
#         'PORT':'3306',
#         'USER':'admin',
#         'PASSWORD':'admin',
#         'NAME': 'dentistore'
#     }
# }