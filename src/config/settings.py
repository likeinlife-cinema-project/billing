import os

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

include(
    'components/application_definition.py',
    'components/auth_password_validators.py',
    'components/folders.py',
    'components/database.py',
    'components/internationalization.py',
    'components/logging.py',
)

LOCALE_PATHS = ['billing/locale']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_ADMIN_BILLING_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_ADMIN_BILLING_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('DJANGO_ADMIN_BILLING_ALLOWED_HOSTS').split(',')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = [
    '127.0.0.1',
]
