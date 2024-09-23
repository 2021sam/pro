# development.py
from .settings import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

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