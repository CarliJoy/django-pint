=========
Changelog
=========

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
.. _black: https://github.com/psf/black
