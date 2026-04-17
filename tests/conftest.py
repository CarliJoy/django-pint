"""
conftest.py for django_pint tests.

Provides a session-scoped PostgreSQL testcontainer that replaces the need
for a separately running database (Docker service, tox-docker, etc.).
"""

import pytest


@pytest.fixture(scope="session")
def django_db_setup(django_test_environment, django_db_blocker):
    """Start a PostgreSQL container and wire it into Django's test database setup."""
    from django.conf import settings
    from django.test.utils import setup_databases, teardown_databases

    from testcontainers.postgres import PostgresContainer

    with PostgresContainer("postgres:16-alpine") as postgres:
        settings.DATABASES["default"].update(
            {
                "HOST": postgres.get_container_host_ip(),
                "PORT": postgres.get_exposed_port(5432),
                "NAME": postgres.dbname,
                "USER": postgres.username,
                "PASSWORD": postgres.password,
            }
        )

        with django_db_blocker.unblock():
            old_config = setup_databases(verbosity=0, interactive=False)

        yield

        with django_db_blocker.unblock():
            teardown_databases(old_config, verbosity=0)
