=========
Changelog
=========

Version 1.0.2
=============
- Fix broken pipeline for PyPI Sigstore uploads. No source code changes.

Version 1.0.1
=============
- Fix Problem in Publish Pipeline using old upload-artifact (no source code changes)

Version 1.0.0
=============
- Start following `SemVer <https://semver.org/spec/v2.0.0.html>`_
- Convert numeric types to str before calling Decimal `#101 by @mmarra <https://github.com/CarliJoy/django-pint/pull/101>`_
- Try unit conversion instead of literal dimensionality check `#108  by @SamuelJennings <https://github.com/CarliJoy/django-pint/pull/108>`_
- Drop support for Python 3.8 and 3.9 and Django 3.2
- Add support for Python 3.12, 3.13 and 3.14 and Django 6.0 `#116 by @Adiorz <https://github.com/CarliJoy/django-pint/pull/117>`_
- Modernize project setup: Use ``pyproject.toml`` only and ``ruff``.

Version 0.7.2
=============
- fix conversion of number input to DecimalField (`issue #106 <https://github.com/CarliJoy/django-pint/issues/106>`_)

Version 0.7.1
=============
-  fix wrong unit display in widget (`issue #43 <https://github.com/CarliJoy/django-pint/issues/43>`_)

Version 0.7.0
=============
- drop support for Django (<3.2) and Python Versions (<3.7) as they reached EOL
- add ``PositiveIntegerQuantityField`` (`merge request #39 from jwygoda`_)
- fix display of negative and scientific numbers in Widget (`merger request #41 from mikeford3`_)

Version 0.6.3
=============
- fix error with Django 3.2 (`issue #36`_)
- remove PrecisionError
- restructure function a bit, add more type annotations

Version 0.6.2
=============
- only a internal technical release as the PyPi token had to be removed
  due to security breach before and no new token was set before
  releasing 0.6.1

Version 0.6.1
=============
- Fix wrong mixin type for ``DecimalQuantityFormField`` (`merge request #31 from ikseek`_)
- Fix ``BigIntegerQuantityField`` and ``IntegerQuantityField`` showing wrong widget in django admin `issue #34`_

Version 0.6
===========
- Added ``DecimalQuantityField``
- Improved Testing a lot, the different field types are tested individually.
  Now we have a total of 142 tests covering 98% of the code.

Version 0.5
===========
- API Change: Units are now defined project wide in settings and not by defining ureg
  for Fields
- Change of Maintainer to `Carli* Freudenberg`_
- Ported code to work with current version of Django (2.2., 3.0, 3.2) and Python (3.6 - 3.9)
- added test for merge requests
- use `black`_ to format code
- using pytest instead of deprecated django-nose
- Allow custom ureg and integer unit field (`merge request #11 from jonashaag`_)
- pass base_unit from field to widget (`merge request #5 from cornelv`_)
- now using PyScaffold for versioned release
- added documentation and uploaded to readthedocs.org
- using pre-commit (also in CI)
- improved travis ci builds
- Created Changelog file

Version 0.4
===========

- Last release of Maintainer `Ben Harling`_


.. _Ben Harling: https://github.com/bharling
.. _Carli* Freudenberg: https://github.com/CarliJoy
.. _merge request #11 from jonashaag: https://github.com/CarliJoy/django-pint/pull/11
.. _merge request #5 from cornelv: https://github.com/CarliJoy/django-pint/pull/5
.. _merge request #31 from ikseek: https://github.com/CarliJoy/django-pint/pull/31
.. _issue #34: https://github.com/CarliJoy/django-pint/issues/34
.. _black: https://github.com/psf/black
.. _issue #36: https://github.com/CarliJoy/django-pint/issues/36
.. _merge request #39 from jwygoda: https://github.com/CarliJoy/django-pint/pull/39
.. _merger request #41 from mikeford3: https://github.com/CarliJoy/django-pint/issues/40
