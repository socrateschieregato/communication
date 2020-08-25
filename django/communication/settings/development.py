from .base import *  # noqa

DEBUG = True

BASE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_PATH, 'database.sqlite'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
