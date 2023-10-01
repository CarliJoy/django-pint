import os
from pathlib import Path
from pint import UnitRegistry

# Try to find guess the correct loading string for the dummy app,
# which dependes on the PYTHON_PATH (that can differ between local
# testing and a pytest run.
dummy_app_load_string: str = ""
try:
    import tests.dummyapp
except ImportError:
    try:
        import dummyapp
    except ImportError:
        raise ImportError(
            "Neither `tests.dummyapp' nor 'dummyapp' has been "
            " found in the PYTHON_PATH."
        )
    else:
        dummy_app_load_string = "dummyapp"
else:
    dummy_app_load_string = "tests.dummyapp"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
DEBUG = True
STATIC_URL = "/static/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "USER": os.environ.get("POSTGRES_USER", "django_pint"),
        "NAME": os.environ.get("POSTGRES_DB", "django_pint"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get(
            "POSTGRES_PORT", os.environ.get("POSTGRES_5432_TCP_PORT", "")
        ),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "not_secure_in_testing"),
        "TEST": {
            "NAME": os.environ.get("TEST_DB", "mytestdatabase"),
        },
    },
}

# not very secret in tests
SECRET_KEY = "5tb#evac8q447#b7u8w5#yj$yq3%by!a-5t7$4@vrj$al1-u3c"
USE_I18N = True
USE_L10N = True
# Use common Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "quantityfield",
    dummy_app_load_string,
]
ROOT_URLCONF = f"{dummy_app_load_string}.urls"

custom_ureg = UnitRegistry()
custom_ureg.define("custom = [custom]")
custom_ureg.define("kilocustom = 1000 * custom")

DJANGO_PINT_UNIT_REGISTER = custom_ureg

WSGI_APPLICATION = f"{dummy_app_load_string}.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
