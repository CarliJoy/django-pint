import pathlib
import tempfile

import nox

# Use uv as the venv backend
nox.options.default_venv_backend = "uv"

# Python versions supported per Django version
DJANGO_52_PYTHON_VERSIONS = ["3.10", "3.11", "3.12", "3.13"]
DJANGO_60_PYTHON_VERSIONS = ["3.12", "3.13", "3.14"]

# Cache the built wheel across all sessions within a single nox invocation.
_wheel: pathlib.Path | None = None


def _build_wheel(session: nox.Session) -> pathlib.Path:
    """Build the project wheel once and return its Path, reusing on subsequent calls."""
    global _wheel
    if _wheel is None:
        dist_dir = pathlib.Path(tempfile.mkdtemp(prefix="nox-wheel-"))
        session.run("uv", "build", "--wheel", "--out-dir", str(dist_dir), external=True)
        (_wheel,) = dist_dir.glob("*.whl")
    return _wheel


def _run_tests(session: nox.Session, django_constraint: str) -> None:
    """Build the wheel (once) and run the test suite against it."""
    wheel = _build_wheel(session)
    session.install("--group", "testing", django_constraint, str(wheel))
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
    session.install("--group", "docs", str(wheel))
    session.run("sphinx-build", "-b", "doctest", "docs", "docs/_build/doctest")
