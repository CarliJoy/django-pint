from pint import UnitRegistry

# Allow user specific postgres credentials to be provided
# in a local.py file
try:
    from .local import PG_PASSWORD, PG_USER
except ImportError:
    # Define the defaults Travis CI/CD if any parameter was unset
    PG_USER = "django_pint"
    PG_PASSWORD = "not_secure_in_testing"

try:
    from .local import PG_DATABASE
except ImportError:
    PG_DATABASE = "django_pint"

try:
    from .local import PG_HOST
except ImportError:
    PG_HOST = "localhost"

try:
    from .local import PG_PORT
except ImportError:
    PG_PORT = ""

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "USER": PG_USER,
        "NAME": PG_DATABASE,
        "HOST": PG_HOST,
        "PORT": PG_PORT,
        "PASSWORD": PG_PASSWORD,
        "TEST": {
            "NAME": "mytestdatabase",
        },
    },
}

# not very secret in tests
SECRET_KEY = "5tb#evac8q447#b7u8w5#yj$yq3%by!a-5t7$4@vrj$al1-u3c"
USE_I18N = True
USE_L10N = True
# Use common Middleware
MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
)
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "quantityfield",
    "tests.dummyapp",
]


custom_ureg = UnitRegistry()
custom_ureg.define("custom = [custom]")
custom_ureg.define("kilocustom = 1000 * custom")

DJANGO_PINT_UNIT_REGISTER = custom_ureg
