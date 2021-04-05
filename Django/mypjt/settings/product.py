from .base import *

ALLOWED_HOST = ['*']

SECRET_KEY = '-qrg&jjb8aq(s8n3ae6rqv(%528_e#h-k(e7qudka9ntseh^kr'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '3jo',
        'USER': '3jo',
        'PASSWORD': '3jo',
        'HOST': 'db',
        'PORT': '3306',
    }
}
