from pathlib import Path
import constants
BASE_DIR = Path(__file__).resolve().parent.parent
import os
from gqlauth.settings_type import GqlAuthSettings
from strawberry.annotation import StrawberryAnnotation
from strawberry.field import StrawberryField

SECRET_KEY = constants.SECRET

DEBUG = True

ALLOWED_HOSTS = ['localhost', constants.SITE_HOST, '127.0.0.1']


INSTALLED_APPS = [
    'modeltranslation',
    'daphne',
    'adminactions',
    'django_admin_index',
    'ordered_model',
    'jazzmin',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'strawberry_django',
    "main",
    'channels',
    "tinymce",
    "import_export",
    'debug_toolbar',
    'corsheaders',
    'gqlauth',
    'defender',
    'rest_framework',
    'djangoql',
]

DEFENDER_REDIS_URL = f'{constants.REDIS_HOST}/0'
DEFENDER_BEHIND_REVERSE_PROXY = True

AUTH_USER_MODEL = 'main.UserModel'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "gqlauth.core.middlewares.django_jwt_middleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",   
    'strawberry_django.middlewares.debug_toolbar.DebugToolbarMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'defender.middleware.FailedLoginMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

GQL_AUTH = GqlAuthSettings(
    LOGIN_REQUIRE_CAPTCHA=False,
    ALLOW_LOGIN_NOT_VERIFIED=True,
    REGISTER_REQUIRE_CAPTCHA=False,
    SEND_ACTIVATION_EMAIL=False,
    LOGIN_FIELDS= [StrawberryField(python_name="tg_id", type_annotation=StrawberryAnnotation(str))],
    REGISTER_MUTATION_FIELDS= [StrawberryField(python_name="tg_id", type_annotation=StrawberryAnnotation(str))],
    JWT_PAYLOAD_PK=StrawberryField(python_name="tg_id", type_annotation=StrawberryAnnotation(str)),
)

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ['http://localhost:8080']

INTERNAL_IPS = [
    '127.0.0.1',
]

ROOT_URLCONF = "back.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = "back.wsgi.application"
ASGI_APPLICATION = 'back.asgi.application'

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': constants.DB_NAME,
        'USER': constants.DB_LOGIN,
        'PASSWORD': constants.DB_PASSWORD,
        'HOST': constants.DB_HOST,
        'PORT': constants.DB_PORT
    }
}

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

LANGUAGE_CODE = "ru"

TIME_ZONE = "Asia/Tashkent"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = "static/"
MEDIA_URL = "media/"
MEDIA_ROOT = "media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
gettext = lambda s: s
LANGUAGES = (
  ('ru', gettext('Russia')),
)

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale/"), )

STRAWBERRY_DJANGO = {
    "FIELD_DESCRIPTION_FROM_HELP_TEXT": True,
    "TYPE_DESCRIPTION_FROM_MODEL_DOCSTRING": True,
    "MUTATIONS_DEFAULT_ARGUMENT_NAME": "input",
    "MUTATIONS_DEFAULT_HANDLE_ERRORS": True,
    "GENERATE_ENUMS_FROM_CHOICES": False,
    "MAP_AUTO_ID_AS_GLOBAL_ID": True,
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
