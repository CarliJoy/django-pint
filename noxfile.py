import nox

# Use uv as the default venv backend for speed; fall back to virtualenv if uv is absent
nox.options.default_venv_backend = "uv|virtualenv"

# Python versions supported per Django version
DJANGO_52_PYTHON_VERSIONS = ["3.10", "3.11", "3.12", "3.13"]
DJANGO_60_PYTHON_VERSIONS = ["3.12", "3.13", "3.14"]

TEST_DEPS = [
    "pytest",
    "pytest-cov",
    "pytest-django",
    "testcontainers[postgres]",
    "psycopg2-binary",
]


def _run_tests(session: nox.Session, django_constraint: str) -> None:
    """Install dependencies and run the test suite."""
    session.install(*TEST_DEPS, django_constraint, "-e", ".")
    session.run("pytest", *session.posargs)


@nox.session(python=DJANGO_52_PYTHON_VERSIONS)
def tests_django52(session: nox.Session) -> None:
    """Run the test suite against Django 5.2."""
    _run_tests(session, "Django>=5.2,<5.3")


@nox.session(python=DJANGO_60_PYTHON_VERSIONS)
def tests_django60(session: nox.Session) -> None:
    """Run the test suite against Django 6.0."""
    _run_tests(session, "Django>=6.0,<6.1")


@nox.session(python="3.12")
def docs_doctest(session: nox.Session) -> None:
    """Run Sphinx doctest on usage examples in docs/."""
    session.install(
        "Django>=5.2",
        "pint>=0.16",
        "sphinx",
        "sphinx-rtd-theme>=0.5.0",
        "m2r2>=0.2.5",
        "recommonmark>=0.6.0",
        "-e",
        ".",
    )
    session.run("sphinx-build", "-b", "doctest", "docs", "docs/_build/doctest")
