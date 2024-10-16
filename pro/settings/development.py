# development.py
from .settings import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

import os
from django.core.management.utils import get_random_secret_key

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', get_random_secret_key())



# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#         'authenticate': {  # Enable logging for the 'user' app
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     },
# }