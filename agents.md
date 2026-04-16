# Agent Guidelines for django-pint

This file provides instructions and conventions for AI coding agents working in this repository.

## Changelog

- **Always** update `CHANGELOG.rst` when making user-visible changes (bug fixes, new features, deprecations, breaking changes, etc.).
- New, unreleased changes go under an `Unreleased` section at the top of the file, above all versioned sections:
  ```rst
  Unreleased
  ==========
  - Your change here
  ```
- Include a link to the related pull request and/or issue when available, following the existing RST link style:
  ```rst
  - Fix foo bar (`#123 <https://github.com/CarliJoy/django-pint/pull/123>`_)
  - Fix baz (`issue #99 <https://github.com/CarliJoy/django-pint/issues/99>`_)
  ```

## Code Style

- Run `pre-commit run --all-files` after making changes to ensure formatting and linting pass before committing.
- The project uses `ruff` for linting and formatting (configured in `pyproject.toml`).

## Testing

- Run tests with `tox` or `pytest` (see `tox.ini` and `pyproject.toml` for configuration).
- Add or update tests for every bug fix or new feature.

## Project Structure

- Source code lives in `src/quantityfield/`.
- Tests live in `tests/`.
- Documentation lives in `docs/`.
