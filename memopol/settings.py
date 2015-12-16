"""
Django settings for memopol project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from socket import gethostname

from django.conf import global_settings
from django.utils.crypto import get_random_string

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.environ.get('OPENSHIFT_DATA_DIR', 'data')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

LOG_DIR = os.environ.get('OPENSHIFT_LOG_DIR', 'log')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

PUBLIC_DIR = os.path.join(
    os.environ.get(
        'OPENSHIFT_REPO_DIR',
        ''),
    'wsgi/static')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_FILE = os.path.join(DATA_DIR, 'secret.txt')

if not os.path.exists(SECRET_FILE):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    with open(SECRET_FILE, 'w+') as f:
        f.write(get_random_string(50, chars))

with open(SECRET_FILE, 'r') as f:
    SECRET_KEY = f.read()


DEBUG = os.environ.get('DJANGO_DEBUG', False)
TEMPLATE_DEBUG = DEBUG
LOG_LEVEL = os.environ.get('DJANGO_LOG_LEVEL', 'INFO')

if SECRET_KEY == 'notsecret' and not DEBUG:
    raise Exception('Please export DJANGO_SECRET_KEY or DEBUG')

ALLOWED_HOSTS = [
    gethostname(),
]

DNS = os.environ.get('OPENSHIFT_APP_DNS', None),
if DNS:
    ALLOWED_HOSTS += DNS

if 'DJANGO_ALLOWED_HOSTS' in os.environ:
    ALLOWED_HOSTS += os.environ.get('DJANGO_ALLOWED_HOSTS').split(',')

REDIS_DB = os.environ.get('REDIS_DB', 1)
ORGANIZATION_NAME = os.environ.get('ORGANIZATION', 'Memopol Demo')

INSTALLED_APPS = (
    # 'django.contrib.admin',
    'autocomplete_light',
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # 3rd party apps
    'compressor',
    'constance',
    'constance.backends.database',
    'bootstrap3',
    'datetimewidget',
    'django_filters',
    'taggit',
    # ---
    'core',
    'representatives',
    'representatives_votes',
    'legislature',
    'votes',
    'positions',
)

if DEBUG:
    try:
        import debug_toolbar  # noqa
    except:
        pass
    else:
        INSTALLED_APPS += ('debug_toolbar',)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'memopol.urls'

WSGI_APPLICATION = 'memopol.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'NAME': os.environ.get('DJANGO_DATABASE_DEFAULT_NAME', 'db.sqlite'),
        'USER': os.environ.get('DJANGO_DATABASE_DEFAULT_USER', ''),
        'PASSWORD': os.environ.get('DJANGO_DATABASE_DEFAULT_PASSWORD', ''),
        'HOST': os.environ.get('DJANGO_DATABASE_DEFAULT_HOST', ''),
        'PORT': os.environ.get('DJANGO_DATABASE_DEFAULT_PORT', ''),
        'ENGINE': os.environ.get('DJANGO_DATABASE_DEFAULT_ENGINE',
                                 'django.db.backends.sqlite3'),

    }
}

if 'OPENSHIFT_DATA_DIR' in os.environ:
    DATABASES['default']['NAME'] = os.path.join(DATA_DIR, 'db.sqlite')

if 'OPENSHIFT_POSTGRESQL_DB_HOST' in os.environ:
    DATABASES['default']['NAME'] = os.environ['OPENSHIFT_APP_NAME']
    DATABASES['default']['USER'] = os.environ[
        'OPENSHIFT_POSTGRESQL_DB_USERNAME']
    DATABASES['default']['PASSWORD'] = os.environ[
        'OPENSHIFT_POSTGRESQL_DB_PASSWORD']
    DATABASES['default']['HOST'] = os.environ['OPENSHIFT_POSTGRESQL_DB_HOST']
    DATABASES['default']['PORT'] = os.environ['OPENSHIFT_POSTGRESQL_DB_PORT']
    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = os.environ.get('DJANGO_LANGUAGE_CODE', 'en-us')

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_URL = '/static/'
COMPRESS_ROOT = 'static/'

if DATA_DIR:
    MEDIA_URL = '/static/media/'
    MEDIA_ROOT = os.path.join(DATA_DIR, 'media')

if PUBLIC_DIR:
    STATIC_URL = '/static/collected/'
    STATIC_ROOT = os.path.join(PUBLIC_DIR, 'collected')

# HAML Templates
# https://github.com/jessemiller/hamlpy

TEMPLATE_DIRS = (
    'core/templates',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'hamlpy.template.loaders.HamlPyFilesystemLoader',
    'hamlpy.template.loaders.HamlPyAppDirectoriesLoader',
)

"""
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'hamlpy.template.loaders.HamlPyFilesystemLoader',
        'hamlpy.template.loaders.HamlPyAppDirectoriesLoader',
    )),
)
"""

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'constance.context_processors.config',
    'django.template.context_processors.request',
)

# Static files finders


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # Compressor finder
    'compressor.finders.CompressorFinder',
)

# Use compressor even in debug
COMPRESS_ENABLED = False

COMPRESS_PRECOMPILERS = (
    # ('text/coffeescript', 'coffee --compile --stdio'),
    ('text/less', 'lesscpy {infile}'),
    # ('text/x-sass', 'sass {infile} {outfile}'),
    # ('text/x-scss', 'sass --scss {infile} {outfile}'),
    # ('text/stylus', 'stylus < {infile} > {outfile}'),
    # ('text/foobar', 'path.to.MyPrecompilerFilter'),
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s[%(module)s]: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'memopol': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
        },
        'representatives': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
        },
        'representatives_votes': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
        }
    },
}

if DEBUG:
    LOGGING['handlers']['debug'] = {
        'level': 'DEBUG',
        'class': 'logging.FileHandler',
        'filename': os.path.join(LOG_DIR, 'debug.log'),
    }
    for logger in LOGGING['loggers'].values():
        logger['handlers'].append('debug')

RAVEN_FILE = os.path.join(DATA_DIR, 'sentry')
if os.path.exists(RAVEN_FILE):
    INSTALLED_APPS += ('raven.contrib.django.raven_compat',)

    LOGGING['handlers']['sentry'] = {
        'level': 'INFO',
        'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
    }
    LOGGING['loggers']['sentry.errors'] = LOGGING['loggers']['raven'] = {
        'level': 'INFO',
        'handlers': ['console'],
        'propagate': False,
    }

    with open(RAVEN_FILE, 'r') as f:
        RAVEN_CONFIG = {
            'dsn': f.read().strip()
        }

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {
    'USE_COUNTRY': (True, 'Use country for representative'),
    'MAIN_GROUP_KIND': ('group', 'Main group kind'),
    'ORGANIZATION_NAME': ('La Quadrature du Net', 'Organization name'),
}
