"""
Django settings for userManagement project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import keycloak
from keycloak import KeycloakAdmin
from keycloak import KeycloakOpenIDConnection
from rest_framework import authentication


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-oi11xym#@+&qvb6g7a92d!a8h$qdzb@$s&tn!81h)a8m74i1&i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
        'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'userApp',
    'rest_framework_swagger',
   # 'keycloak_oidc',
   # 'oauth2_provider',
]

KEYCLOAK_CONFIG= {
        'CLIENT_ID':'admin-cli',
        'REALM':'master',
        'KEYCLOAK_URL':'https://10.63.35.142:8080/auth',
        }
#AUTHENTICATION_CLASSES=(
 #       'keycloak_oidc.auth.OIDCAuthentication',
 #     )
#OAUTH2_PROVIDER ={
 #   'OAUTH2_BACKEND_CLASS' :'keycloak_oidc.backends.KeycloakOIDCAuth',
  #  'SCOPES': {
   #     'read': 'Read scope',
    #    'write': 'Write scope'
   # },
#}
KEYCLOAK_SERVER_URL ='http://10.63.35.142:8080'
KEYCLOAK_REALM = 'master'
KEYCLOAK_CLIENT_ID = 'admin-cli'
KEYCLOAK_ADMIN_USERNAME = 'admin'
KEYCLOAK_ADMIN_PASSWORD = 'tcs123'
KEYCLOAK_CLIENTID = '70465e9a-368b-44ad-8f84-b9d48c8dcb12'
#KEYCLOAK_OIDC_CLIENT_SECRET= 'XTTYVcN2GeOlPFT6BZYcBEV5YCBT09n7'

DEBUG = True

MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'userManagement.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'userManagement.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]

ALLOWED_HOSTS=['*']
CORS_ORIGIN_ALLOW_ALL = True
APPEND_SLASH=False
