# See https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cmb_sample.settings')
application = get_wsgi_application()
