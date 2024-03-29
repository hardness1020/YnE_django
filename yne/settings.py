import io
import os

import environ
from google.cloud import secretmanager
from google.oauth2 import service_account


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(DEBUG=(bool, False))
env_file = os.path.join(BASE_DIR, ".env")

if os.path.isfile(env_file):
    env.read_env(env_file)
elif os.getenv("TRAMPOLINE_CI", None):
    # not working because lack of firebase config, must have .env file
    placeholder = (
        f"SECRET_KEY=a\n"
        "GS_BUCKET_NAME=None\n"
        f"DATABASE_URL=sqlite://{os.path.join(BASE_DIR, 'db.sqlite3')}\n"
        "DEBUG=True\n"
    )
    env.read_env(io.StringIO(placeholder))
elif os.environ.get("GOOGLE_CLOUD_PROJECT", None):
    # Pull secrets from Google Secret Manager
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    
    # Get the credentials from the environment file which is downloaded from GCP IAM
    credentials = service_account.Credentials.from_service_account_file(
        os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    )

    # Use the credentials to create a client to access the secret manager from GCP project
    client = secretmanager.SecretManagerServiceClient(credentials=credentials)
    settings_name = os.environ.get("SETTINGS_NAME", "yne_django_settings")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

    env.read_env(io.StringIO(payload))
else:
    raise Exception("No local .env or TRAMPOLINE_CI or GOOGLE_CLOUD_PROJECT detected. No secrets found.")



SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")


# SECURITY WARNING: App Engine's security features ensure that it is safe to
# have ALLOWED_HOSTS = ['*'] when the app is deployed. If you deploy a Django
# app not on App Engine, make sure to set an appropriate host here.
ALLOWED_HOSTS = ["*"]


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "channels",
    
    'yne.auth_firebase.apps.AuthFirebaseConfig',
    'yne.django_user.apps.DjangoUserConfig',
    'yne.activity.apps.ActivityConfig',
    # "yne.auth_firebase",
    # "yne.django_user",
    # "yne.activity",
    # "chat",
]

# Test for authentication
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'auth_firebase.authentication.FirebaseAuthentication',
#     ),
# }
#

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "yne.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]



# WSGI config 
WSGI_APPLICATION = "yne.wsgi.application"

# ASGI config
ASGI_APPLICATION = "yne.asgi.application"
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(os.getenv('REDIS_HOST', 'redis'), 6379)],
        },
    },
}


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {"default": env.db()}

# If the flag as been set, configure to use proxy
if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 5432
    
# Use a in-memory sqlite3 database when testing in CI systems
if os.getenv("TRAMPOLINE_CI", None):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {   
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Taipei"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# Define static storage via django-storages[google]
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "yne","static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "yne", "media")

if os.getenv("TRAMPOLINE_CI", None):
    # collect the static files in following path to STATIC_ROOT
    STATICFILES_DIRS = [
        # os.path.join(BASE_DIR, "static"),
    ]
else:
    GS_BUCKET_NAME = env("GS_BUCKET_NAME")
    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    GS_DEFAULT_ACL = "publicRead"


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Firebase config
FIREBASE_ACCOUNT_TYPE = env('FIREBASE_ACCOUNT_TYPE')
FIREBASE_PROJECT_ID = env('FIREBASE_PROJECT_ID')
FIREBASE_PRIVATE_KEY_ID = env('FIREBASE_PRIVATE_KEY_ID')
FIREBASE_PRIVATE_KEY = env('FIREBASE_PRIVATE_KEY')
FIREBASE_CLIENT_EMAIL = env('FIREBASE_CLIENT_EMAIL')
FIREBASE_CLIENT_ID = env('FIREBASE_CLIENT_ID')
FIREBASE_AUTH_URI = env('FIREBASE_AUTH_URI')
FIREBASE_TOKEN_URI = env('FIREBASE_TOKEN_URI')
FIREBASE_AUTH_PROVIDER_X509_CERT_URL = env('FIREBASE_AUTH_PROVIDER_X509_CERT_URL')
FIREBASE_CLIENT_X509_CERT_URL = env('FIREBASE_CLIENT_X509_CERT_URL')
# FIREBASE_TEST_USER_UID = env('FIREBASE_TEST_USER_UID')
# FIREBASE_TEST_USER_EMAIL = env('FIREBASE_TEST_USER_EMAIL')
# FIREBASE_TEST_USER_PASSWORD = env('FIREBASE_TEST_USER_PASSWORD')