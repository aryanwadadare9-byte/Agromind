# from pathlib import Path
# BASE_DIR = Path(__file__).resolve().parent.parent
# SECRET_KEY = 'agro-secret-key-change-in-production'
# DEBUG = True
# ALLOWED_HOSTS = ['*']
# INSTALLED_APPS = [
#     'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
#     'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
#     'users','farm','disease','market','organic','rainfall','news','ai_engine',
# ]
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]
# ROOT_URLCONF = 'agro.urls'
# TEMPLATES = [{'BACKEND':'django.template.backends.django.DjangoTemplates',
#     'DIRS':[BASE_DIR/"templates"],'APP_DIRS':True,
#     'OPTIONS':{'context_processors':[
#         'django.template.context_processors.debug',
#         'django.template.context_processors.request',
#         'django.contrib.auth.context_processors.auth',
#         'django.contrib.messages.context_processors.messages',
#     ]},
# }]
# DATABASES = {"default": {
#     "ENGINE": "django.db.backends.postgresql",
#     "NAME": "agro_db",
#     "USER": "postgres",
#     "PASSWORD": "your_db_password",
#     "HOST": "localhost",
#     "PORT": "5432",
# }}
# # ── API KEYS ──
# OPENROUTER_API_KEY ="api  keuy for openrouter.ai"
# OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
# STEPFUN_MODEL = "stepfun/step-3.5-flash"
# GEMINI_MODEL = "google/gemini-2.0-flash-001"
# # Open-Meteo is FREE — no key needed!

# MEDIA_URL = "/media/"
# MEDIA_ROOT = BASE_DIR / "media"
# STATIC_URL = "/static/"
# STATICFILES_DIRS = [BASE_DIR / "static"]
# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# LOGIN_URL = "/users/login/"
# LOGIN_REDIRECT_URL = "/farm/"

import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Required environment variables on Render:
# SECRET_KEY, DATABASE_URL, OPENROUTER_API_KEY
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-key-change-me")
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if render_host:
    ALLOWED_HOSTS.append(render_host)

CSRF_TRUSTED_ORIGINS = []
if render_host:
    CSRF_TRUSTED_ORIGINS.append(f"https://{render_host}")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "users",
    "farm",
    "disease",
    "market",
    "organic",
    "rainfall",
    "news",
    "ai_engine",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "agro.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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


DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
    )
}


OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
STEPFUN_MODEL = "stepfun/step-3.5-flash"
GEMINI_MODEL = "google/gemini-2.0-flash-001"


MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "/users/login/"
LOGIN_REDIRECT_URL = "/farm/"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
