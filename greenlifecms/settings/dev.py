from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=c1cu+xrtzdpf0fj$i058y)ea&m(%=e&e4w5*nryu(u5@s&_#c'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 


try:
    from .local import *
except ImportError:
    pass
