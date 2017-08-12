# Django settings for doroko project.

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from settings_local import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

THUMBNAIL_DEBUG = True

ADMINS = (
     ('Admin', 'admin@sellbig.in'),
)

MANAGERS = ADMINS
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'sb_db',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'djangouser',
        'PASSWORD': 'pl@n3tv3nus',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
        'OPTIONS'  : { 'init_command' : 'SET storage_engine=MYISAM', },
    }
}
"""
DATABASES = {
	'default': {
		#'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'ENGINE': 'django.contrib.gis.db.backends.postgis',
		'NAME': 'sb_db_p',
		'USER': 'djangouser',
		'PASSWORD': 'pl@n3tv3nus',
		'HOST': 'localhost',
		'PORT': '',
	}
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
'127.0.0.1'
]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Kolkata'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
#MEDIA_ROOT = '/home/deep/work/doroko/media/'
MEDIA_ROOT = (os.path.join(BASE_DIR, "media"))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = (os.path.join(BASE_DIR, "static"))#''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
#STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
#)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '0a=y#5)nk+^ixr2#hj97$4#)wfdt-_!+c3qbkac+_j)&vgq_lq'

"""# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)"""

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'doroko.urls'

# Provide login where to land after logging in
LOGIN_REDIRECT_URL = '/'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'doroko.wsgi.application'


"""TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/deep/work/doroko/templates',
    #os.path.join(BASE_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS =(
	'django.contrib.auth.context_processors.auth',
	'django.contrib.messages.context_processors.messages',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'django.core.context_processors.static',
	'django.core.context_processors.tz',
	'django.core.context_processors.request',
	'account.context_processors.notifications',
	'django_facebook.context_processors.facebook',
)"""

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',                
                'account.context_processors.notifications',
                'django_facebook.context_processors.facebook',
            ],
        },
    },
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.gis',
    'account',
    'friends',
    'talks',
    'feed',
    'messages',
    'sorl.thumbnail',
    'taggit',
    'haystack',
    'endless_pagination',
    'widget_tweaks',
    'cities',
    'django_facebook',
)

AUTHENTICATION_BACKENDS = (
    'django_facebook.auth_backends.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
                'level': 'DEBUG',
                'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'cities': {
                'handlers': ['console'],
                'level': 'INFO'
        },
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
		'INCLUDE_SPELLING': True,

    },
}

# Custom haystack for highlighter
HAYSTACK_CUSTOM_HIGHLIGHTER = 'account.haystack_custom.MyHighlighter'

###
# Imported from settings_local file
# To auto update search indexes
#HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Email settings
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_HOST = 'localhost'
#EMAIL_PORT = 587
#EMAIL_PORT = 25
#EMAIL_HOST_USER = 'deepinder19@gmail.com'
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''
#EMAIL_USE_TLS = True
#EMAIL_USE_TLS = False
#DEFAULT_FROM_EMAIL = 'support@sellbig.in'
###

ENDLESS_PAGINATION_LOADING = """<img src="/static/img/loader.gif" alt="loading..." />"""

# Added following for the django cities issue
CITIES_PLUGINS = []

#GEOS_LIBRARY_PATH = '/home/deep/geos-3.3.8/capi/.libs/libgeos_c.so'
GEOS_LIBRARY_PATH = os.path.join(BASE_DIR, 'geos-3.3.8/capi/.libs/libgeos_c.so')

# for django-facebook
AUTH_USER_MODEL = 'django_facebook.FacebookCustomUser'
FACEBOOK_STORE_FRIENDS = True

###
# Commented for production - test app used for local
#FACEBOOK_APP_ID = '415278271918510'
#FACEBOOK_APP_SECRET = '35660ba14928d68b9b258022f533193f'
#FACEBOOK_APP_ID = '813642928748707'
#FACEBOOK_APP_SECRET = 'cd8575bde43f02cdb8beaf9c5c099085'
###

FACEBOOK_DEFAULT_SCOPE = ['email', 'user_friends']

# Reserved Url's
RESERVED_URLS = (
				'autocomplete_city',
				'autocomplete_tag',
				'find_friends',
				'invite_friends',
				'facebook',
				'notifications',
				'bar_notifications',
				'wishbox',
				'owned_stuff',
				'profile',
				'office',
				'switch',
				'edit_business',
				'image',
				'billboard',
				'business_logo',
				'talks',
				'search',
				'admin',
				'messages',
				'friends',
				'business',
				'policy',
				'terms',
				'about',
				'contact',
				)
