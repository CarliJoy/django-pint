import functools
import pathlib
import subprocess

import nox

# Use uv as the venv backend
nox.options.default_venv_backend = "uv"

# Python versions supported per Django version
DJANGO_52_PYTHON_VERSIONS = ["3.10", "3.11", "3.12", "3.13"]
DJANGO_60_PYTHON_VERSIONS = ["3.12", "3.13", "3.14"]

_DIST_DIR = pathlib.Path("dist")
_SRC_DIR = pathlib.Path("src")


def _src_max_mtime() -> float:
    """Return the most recent modification time of any file under src/."""
    return max(
        (p.stat().st_mtime for p in _SRC_DIR.rglob("*") if p.is_file()),
        default=0.0,
    )


@functools.cache
def _build_wheel() -> pathlib.Path:
    """Build the project wheel into dist/, rebuilding only when source files are newer."""
    _DIST_DIR.mkdir(exist_ok=True)
    src_mtime = _src_max_mtime()
    existing = sorted(_DIST_DIR.glob("*.whl"), key=lambda p: p.stat().st_mtime)
    # Reuse the most recent wheel if it is already newer than all source files
    if existing and existing[-1].stat().st_mtime >= src_mtime:
        return existing[-1]
    # Remove stale wheels and rebuild
    for w in existing:
        w.unlink()
    subprocess.run(
        ["uv", "build", "--wheel", "--out-dir", str(_DIST_DIR)],
        check=True,
    )
    (wheel,) = _DIST_DIR.glob("*.whl")
    return wheel


def _run_tests(session: nox.Session, django_constraint: str) -> None:
    """Build the wheel (once) and run the test suite against it."""
    wheel = _build_wheel()
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
    wheel = _build_wheel()
    session.install("--group", "docs", str(wheel))
    session.run("sphinx-build", "-b", "doctest", "docs", "docs/_build/doctest")
