
# To auto update search indexes
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'support@sellbig.in'
EMAIL_HOST_PASSWORD = 'pl@n3tplut0'
DEFAULT_FROM_EMAIL = 'support@sellbig.in'

# Facebook app settings
FACEBOOK_APP_ID = '415278271918510'
FACEBOOK_APP_SECRET = '35660ba14928d68b9b258022f533193f'
#FACEBOOK_APP_ID = '813642928748707'
#FACEBOOK_APP_SECRET = 'cd8575bde43f02cdb8beaf9c5c099085'
