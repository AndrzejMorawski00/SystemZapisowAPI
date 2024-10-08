import os
from .settings import *
from .settings import BASE_DIR

ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' else []
CSRF_TRUSTED_ORIGINS = [
    f'https://{os.environ['WEBSITE_HOSTNAME']}'] if 'WEBSITE_HOSTNAME' in os.environ else []
DEBUG = False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    'https://jolly-glacier-0187bfe03.5.azurestaticapps.net']

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

conn_str = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
conn_str_params = {pair.split('=')[0]: pair.split(
    '=')[1] for pair in conn_str.split(' ')}


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": conn_str_params['dbname'],
        "HOST": conn_str_params['host'],
        "USER": conn_str_params['user'],
        "PASSWORD": conn_str_params['password'],
    }
}
