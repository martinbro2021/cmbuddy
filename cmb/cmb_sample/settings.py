import logging
import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from django.core.management.utils import get_random_secret_key

logger = logging.getLogger(__name__)

# Build paths inside the cmb_sample like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

ALLOWED_HOSTS = ["localhost"]

SECRET_KEY = os.environ.get("SECRET_KEY_CMS")
if not SECRET_KEY and not DEBUG:
    raise ImproperlyConfigured("The SECRET_KEY setting must not be empty.")
elif not SECRET_KEY:
    SECRET_KEY = get_random_secret_key()

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

INSTALLED_APPS = [
    'sslserver',
    'tinymce',
    'django_cleanup.apps.CleanupConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    'cmb_home',
    'cmb_contact',
    'cmb_captcha',
    'cmb_calendar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cmb_sample.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [BASE_DIR / 'cmb_sample' / 'templates'],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cmb_sample.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'sample-db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en'
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
APPS_WITH_STATIC_DIRS = ["cmb_captcha", "cmb_contact", "cmb_home", "cmb_sample"]  # only temp
STATICFILES_DIRS = [os.path.join(BASE_DIR, f"{app}/static") for app in APPS_WITH_STATIC_DIRS]
STATICFILES_DIRS.append(os.path.join(BASE_DIR, "cmb_sample/static"))
STATIC_URL = 'static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'rich.logging.RichHandler',
            'rich_tracebacks': True,
            'show_time': True,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}

TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "height": 500,
    "menubar": False,
    "plugins": "advlist,autolink,lists,link,image,charmap,print,preview,anchor,"
    "searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,"
    "code,help,wordcount,hr",
    "toolbar": "undo redo | searchreplace | formatselect | "
    "forecolor backcolor| "
    "alignleft aligncenter alignright alignjustify | "
    "bold italic | link hr | bullist numlist outdent indent | "
    "removeformat | help fullscreen |"
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
if not DEBUG:
    try:
        from cmb_sample import config
        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        EMAIL_HOST = config.EMAIL_HOST
        EMAIL_HOST_USER = config.EMAIL_HOST_USER
        EMAIL_HOST_PASSWORD = config.EMAIL_HOST_PASSWORD
        EMAIL_PORT = config.EMAIL_PORT
        EMAIL_USE_TLS = config.EMAIL_USE_TLS
    except Exception as ex:
        logger.error(ex)
