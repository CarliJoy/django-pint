# -*- coding: utf-8 -*-
"""
    Dummy conftest.py for django_pint.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    https://pytest.org/latest/plugins.html
"""

import django

from pint import UnitRegistry

# Allow user specific postgres credentials to be provided
# in a local.py file
try:
    from .local import PG_PASSWORD, PG_USER
except ImportError:
    # Define the defaults Travis CI/CD if any parameter was unser
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


def pytest_configure(config):
    from django.conf import settings

    custom_ureg = UnitRegistry()
    custom_ureg.define("custom = [custom]")
    custom_ureg.define("kilocustom = 1000 * custom")

    settings.configure(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.postgresql_psycopg2",
                "NAME": PG_DATABASE,
                "USER": PG_USER,
                "PASSWORD": PG_PASSWORD,
                "HOST": PG_HOST,
                "PORT": PG_PORT,
            }
        },
        SECRET_KEY="not very secret in tests",
        USE_I18N=True,
        USE_L10N=True,
        # Use common Middleware
        MIDDLEWARE=(
            "django.middleware.common.CommonMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
        ),
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.admin",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.sites",
            "django.contrib.flatpages",
            "quantityfield",
            "tests.dummyapp",
        ],
        DJANGO_PINT_UNIT_REGISTER=custom_ureg,
    )
    django.setup()
