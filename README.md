
[![Build Status](https://api.travis-ci.com/CarliJoy/django-pint.svg?branch=master)](https://travis-ci.com/github/CarliJoy/django-pint)
[![codecov](https://codecov.io/gh/CarliJoy/django-pint/branch/master/graph/badge.svg?token=I3M4CLILXE)](https://codecov.io/gh/CarliJoy/django-pint)
[![PyPI Downloads](https://img.shields.io/pypi/dm/django-pint.svg?maxAge=2592000?style=plastic)](https://pypistats.org/packages/django-pint)
[![Python Versions](https://img.shields.io/pypi/pyversions/django-pint.svg)](https://pypi.org/project/django-pint/)
[![PyPI Version](https://img.shields.io/pypi/v/django-pint.svg?maxAge=2592000?style=plastic)](https://pypi.org/project/django-pint/)
[![Project Status](https://img.shields.io/pypi/status/django-pint.svg)](https://pypi.org/project/SyncGitlab2MSProject/)
[![Wheel Build](https://img.shields.io/pypi/wheel/django-pint.svg)](https://pypi.org/project/django-pint/)
[![Code Style Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/CarliJoy/django-pint/main.svg)](https://results.pre-commit.ci/latest/github/CarliJoy/django-pint/main)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/django-pint/badge/?version=latest)](https://django-pint.readthedocs.io/en/latest/?badge=latest)

# Django Quantity Field


A Small django field extension allowing you to store quantities in certain units and perform conversions easily. Uses [pint](https://github.com/hgrecco/pint) behind the scenes. Also contains a form field class and form widget that allows a user to choose alternative units to input data. The cleaned_data will output the value in the base_units defined for the field, eg: you specify you want to store a value in grams but will allow users to input either grams or ounces.


## Help wanted
I am currently not working with Django anymore. Therefore the Maintenance of this project is not a priority for me anymore.
If there is anybody that could imagine helping out maintaining the project, send me a mail.

## Compatibility


Requires django >= 5.2, and python 3.10/3.11/3.12/3.13/3.14

Tested with the following combinations:
* Django 5.2 (Python 3.10, 3.11, 3.12, 3.13, 3.14)
* Django 6.0 (Python 3.12, 3.13, 3.14)

## Installation


    pip install django-pint


## Simple Example

Best way to illustrate is with an example

```python
# app/models.py

from django.db import models
from django_pint.fields import QuantityField

class HayBale(models.Model):
    weight = QuantityField('tonne')
```

Quantities are stored as float (Django FloatField) and retrieved like any other field

```python
>>> bale = HayBale.objects.create(weight=1.2)
>>> bale = HayBale.objects.first()
>>> bale.weight
<Quantity(1.2, 'metric_ton')>
>>> bale.weight.magnitude
1.2
>>> bale.weight.units
<Unit('metric_ton')>
>>> bale.weight.to('kilogram')
<Quantity(1200.0, 'kilogram')>
>>> bale.weight.to('pound')  # doctest: +ELLIPSIS
<Quantity(2645.5..., 'pound')>
```

If your base unit is atomic (i.e. can be represented by an integer), you may also use `IntegerQuantityField` and `BigIntegerQuantityField`.

If you prefer exact units you can use the `DecimalQuantityField`

You can also pass Quantity objects to be stored in models. These are automatically converted to the units defined for the field
( but can be converted to something else when retrieved of course ).

```python
>>> from django_pint.units import ureg
>>> Quantity = ureg.Quantity
>>> pounds = Quantity(500 * ureg.pound)
>>> bale = HayBale.objects.create(weight=pounds)
>>> bale = HayBale.objects.last()
>>> bale.weight  # doctest: +ELLIPSIS
<Quantity(0.2267..., 'metric_ton')>
```

Use the inbuilt form field and widget to allow input of quantity values in different units

```python
from django_pint.fields import QuantityFormField

class HayBaleForm(forms.Form):
    weight = QuantityFormField(base_units='gram', unit_choices=['gram', 'ounce', 'milligram'])
```

The form will render a float input and a select widget to choose the units.
Whenever cleaned_data is presented from the above form the weight field value will be a
Quantity with the units set to grams (values are converted from the units input by the user).
You also can add the `unit_choices` directly to the `ModelField`. It will be propagated
correctly.

```python
>>> from django import forms
>>> from django_pint.fields import QuantityFormField
>>> class HayBaleForm(forms.Form):
...     weight = QuantityFormField(base_units='gram', unit_choices=['gram', 'ounce', 'milligram'])
>>> form = HayBaleForm(data={'weight_0': '100', 'weight_1': 'gram'})
>>> form.is_valid()
True
>>> form.cleaned_data['weight']
<Quantity(100.0, 'gram')>
```

For comparative lookups, query values will be coerced into the correct units when comparing values,
this means that comparing 1 ounce to 1 tonne should yield the correct results.

```python
>>> from django_pint.units import ureg
>>> Quantity = ureg.Quantity
>>> bale = HayBale.objects.create(weight=0.3)
>>> HayBale.objects.filter(weight__lt=Quantity(2000 * ureg.pound)).count()
1
```

You can also use a custom Pint unit registry in your project `settings.py`

```python
# project/settings.py

from pint import UnitRegistry

# django-pint will set the DJANGO_PINT_UNIT_REGISTER automatically
# as application_registry
DJANGO_PINT_UNIT_REGISTER = UnitRegistry('your_units.txt')
DJANGO_PINT_UNIT_REGISTER.define('beer_bottle_weight = 0.8 * kg = beer')

# app/models.py

class HayBale(models.Model):
    # now you can use your custom units in your models
    custom_unit = QuantityField('beer')
```

Note: As the [documentation from pint](https://pint.readthedocs.io/en/latest/tutorial.html#using-pint-in-your-projects)
states quite clearly: For each project there should be only one unit registry.
Please note that if you change the unit registry for an already created project with
data in a database, you could invalidate your data! So be sure you know what you are
doing!
Still only adding units should be okay.

## Development

### Preparation

You need [Docker](https://docs.docker.com/get-docker/) — the tests spin up a PostgreSQL container
automatically via [testcontainers](https://testcontainers.com/guides/getting-started-with-testcontainers-for-python/).
No separate database installation is required.

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
2. Fork `django-pint` and clone your fork (see [Tutorial](https://docs.github.com/get-started/quickstart/contributing-to-projects))
3. Change into the repo: `cd django-pint`
4. Install all development dependencies: `uv sync`
5. Activate pre-commit hooks: `uv run pre-commit install`
6. Check that all linters pass: `uv run pre-commit run --all-files`
7. Run the full test suite: `nox`

**Congratulations!** You have successfully set up and tested the upstream version of `django-pint`.

Now you can work on your feature branch and test your changes with `nox`.
Your code will be automatically linted and formatted by `pre-commit` when you commit.
If it fails, add the formatted changes and commit again.

Once you are done, [create a pull request](https://docs.github.com/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork).

### Updating the package
[Python](https://endoflife.date/python) and [Django](https://endoflife.date/django) major versions have defined EOL.
To reduce the maintenance burden and encourage users to use version still receiving security updates any `django-pint` update should match all and only these version of Python and Django that are supported.
Updating these dependencies have to be done in multiple places:
 - `README.md`: Describing it to end users
 - `noxfile.py`: For local testing
 - `pyproject.toml`: For usage with pip and displaying it in PyPi
 - `.github/workflows/test.yaml`: For the CI/CD Definition
