import pathlib

import nox

# Use uv as the venv backend
nox.options.default_venv_backend = "uv"

# Python versions supported per Django version
DJANGO_52_PYTHON_VERSIONS = ["3.10", "3.11", "3.12", "3.13"]
DJANGO_60_PYTHON_VERSIONS = ["3.12", "3.13", "3.14"]


def _build_wheel(session: nox.Session) -> str:
    """Build the project wheel and return the path to the .whl file."""
    dist_dir = session.create_tmp()
    session.run("uv", "build", "--wheel", "--out-dir", dist_dir, external=True)
    (wheel,) = pathlib.Path(dist_dir).glob("*.whl")
    return str(wheel)


def _run_tests(session: nox.Session, django_constraint: str) -> None:
    """Build the wheel and run the test suite against it."""
    wheel = _build_wheel(session)
    session.install("--group", "testing", django_constraint, wheel)
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
    wheel = _build_wheel(session)
    session.install("--group", "docs", wheel)
    session.run("sphinx-build", "-b", "doctest", "docs", "docs/_build/doctest")
