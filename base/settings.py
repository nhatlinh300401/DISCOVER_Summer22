"""
Django settings for base project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# load environment variables
env_path = Path('.') / '.env'
load_dotenv(verbose=True, dotenv_path=env_path)

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
if str(os.getenv('DJANGO_DEBUG')).lower() == 'false':
    DEBUG = False
else:
    DEBUG = True

# MUST be updated for production
ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'mozilla_django_oidc',  # mozilla-django-oidc: https://mozilla-django-oidc.readthedocs.io/en/stable/
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',    
    'crispy_forms',  # django-crispy-forms: https://django-crispy-forms.readthedocs.io/en/latest/dj
    'bootstrap4',  # django-bootstrap4: https://django-bootstrap4.readthedocs.io/en/latest/quickstart.html
    'accounts',  # custom user accounts
    'resources',  # aerpaw resources
    'reservations',  # aerpaw reservations
    'experiments',  # aerpaw experiments
    'projects',  # aerpaw projects
    'profiles',  # aerpaw profiles
    # 'cicd',  # aerpaw cicd (RM_CICD: Deactivate until further notice 8/15/2021)
    'user_groups',  # user_groups
    'usercomms',  # aerpaw user communications
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # 'mozilla_django_oidc.auth.OIDCAuthenticationBackend',   # mozilla-django-oidc - default user model
    'accounts.cilogon_auth.MyOIDCAB',  # mozilla-django-oidc - custom user model
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'mozilla_django_oidc.middleware.SessionRefresh', # TODO: override SessionRefresh to use CILogon tokens
]

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates/base'),
            os.path.join(BASE_DIR, 'templates/projects'),
            os.path.join(BASE_DIR, 'templates/users'),
            os.path.join(BASE_DIR, 'templates/experiments'),
            os.path.join(BASE_DIR, 'templates/reservations'),
            os.path.join(BASE_DIR, 'templates/resources'),
            os.path.join(BASE_DIR, 'templates/profiles'),
            # os.path.join(BASE_DIR, 'templates/cicd'),
            os.path.join(BASE_DIR, 'templates/manage'),
            os.path.join(BASE_DIR, 'templates/usercomms'),
        ],
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'base.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT')
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

# Login/Logout redirects
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# mozilla-django-oidc
# https://mozilla-django-oidc.readthedocs.io/en/stable/index.html

# client id and client secret
OIDC_RP_CLIENT_ID = os.getenv('OIDC_RP_CLIENT_ID', None)
OIDC_RP_CLIENT_SECRET = os.getenv('OIDC_RP_CLIENT_SECRET', None)
# signing algorithm
OIDC_RP_SIGN_ALGO = os.getenv('OIDC_RP_SIGN_ALGO')
OIDC_OP_JWKS_ENDPOINT = os.getenv('OIDC_OP_JWKS_ENDPOINT')
# OpenID Connect provider (CILogon)
OIDC_OP_AUTHORIZATION_ENDPOINT = os.getenv('OIDC_OP_AUTHORIZATION_ENDPOINT')
OIDC_OP_TOKEN_ENDPOINT = os.getenv('OIDC_OP_TOKEN_ENDPOINT')
OIDC_OP_USER_ENDPOINT = os.getenv('OIDC_OP_USER_ENDPOINT')
# CILogon scopes (default: openid email profile org.cilogon.userinfo)
OIDC_RP_SCOPES = os.getenv('OIDC_RP_SCOPES')
# username algorithm
OIDC_USERNAME_ALGO = 'accounts.cilogon_auth.generate_username'
# SameSite prevents the browser from sending this cookie along with cross-site requests
# Safari seems to need this set to None
SESSION_COOKIE_SAMESITE = None
# SessionRefresh expiry
OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS = int(os.getenv('OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS'))

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.getenv('TIME_ZONE')

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = 'static/'
# placeholder for future static imports
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'base/static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default Django logging is WARNINGS+ to console
# so visible via docker-compose logs django
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'mozilla_django_oidc': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
    },
}

# Auth user model (custom user account)
AUTH_USER_MODEL = 'accounts.AerpawUser'

# Django running behind Nginx reverse proxy
USE_X_FORWARDED_HOST = True

# AERPAW Email for development (use only 1 email backend at a time)
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# AERPAW Email for production (use only 1 email backend at a time)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_ADMIN_USER = os.getenv('EMAIL_ADMIN_USER')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# account for Django 3.2 (Warning models.W042)
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

AERPAW_MAP_URL = os.getenv('AERPAW_MAP_URL', None)