# -*- coding: utf-8 -*-
"""
    Dummy conftest.py for django_pint.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    https://pytest.org/latest/plugins.html
"""

import django

from pint import UnitRegistry


def pytest_configure(config):
    from django.conf import settings

    custom_ureg = UnitRegistry()
    custom_ureg.define("custom = [custom]")
    custom_ureg.define("kilocustom = 1000 * custom")

    settings.configure(
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
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
