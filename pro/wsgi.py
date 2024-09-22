import os
from django.core.wsgi import get_wsgi_application

# Check for the environment (default to 'development' if not set)
env = os.getenv('DJANGO_ENV', 'development')

if env == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pro.settings.production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pro.settings.development')

application = get_wsgi_application()
