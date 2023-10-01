
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


Requires django >= 3.2, and python 3.8/3.9/3.10/3.11

Tested with the following combinations:
* Django 3.2 (Python 3.8, 3.9, 3.10, 3.11)
* Django 4.2 (Python 3.8, 3.9, 3.10, 3.11)

## Installation


    pip install django-pint


## Simple Example

Best way to illustrate is with an example

    # app/models.py

    from django.db import models
    from quantityfield.fields import QuantityField

    class HayBale(models.Model):
	    weight = QuantityField('tonne')

Quantities are stored as float (Django FloatField) and retrieved like any other field

    >> bale = HayBale.objects.create(weight=1.2)
    >> bale = HayBale.objects.first()
	>> bale.weight
	<Quantity(1.2, 'tonne')>
	>> bale.weight.magnitude
	1.2
	>> bale.weight.units
	'tonne'
	>> bale.weight.to('kilogram')
	<Quantity(1200, 'kilogram')>
	>> bale.weight.to('pound')
	<Quantity(2645.55, 'pound')>

If your base unit is atomic (i.e. can be represented by an integer), you may also use `IntegerQuantityField` and `BigIntegerQuantityField`.

If you prefer exact units you can use the `DecimalQuantityField`

You can also pass Quantity objects to be stored in models. These are automatically converted to the units defined for the field
( but can be converted to something else when retrieved of course ).

    >> from quantityfield.units import ureg
    >> Quantity = ureg.Quantity
    >> pounds = Quantity(500 * ureg.pound)
    >> bale = HayBale.objects.create(weight=pounds)
    >> bale.weight
    <Quantity(0.226796, 'tonne')>

Use the inbuilt form field and widget to allow input of quantity values in different units

    from quantityfield.fields import QuantityFormField

    class HayBaleForm(forms.Form):
        weight = QuantityFormField(base_units='gram', unit_choices=['gram', 'ounce', 'milligram'])

The form will render a float input and a select widget to choose the units.
Whenever cleaned_data is presented from the above form the weight field value will be a
Quantity with the units set to grams (values are converted from the units input by the user).
You also can add the `unit_choices` directly to the `ModelField`. It will be propagated
correctly.

For comparative lookups, query values will be coerced into the correct units when comparing values,
this means that comparing 1 ounce to 1 tonne should yield the correct results.

    less_than_a_tonne = HayBale.objects.filter(weight__lt=Quantity(2000 * ureg.pound))

You can also use a custom Pint unit registry in your project `settings.py`

    # project/settings.py

    from pint import UnitRegistry

    # django-pint will set the DJANGO_PINT_UNIT_REGISTER automatically
    # as application_registry
    DJANGO_PINT_UNIT_REGISTER = UnitRegistry('your_units.txt')
    DJANGO_PINT_UNIT_REGISTER.define('beer_bootle_weight = 0.8 * kg = beer')

    # app/models.py

    class HayBale(models.Model):
        # now you can use your custom units in your models
        custom_unit = QuantityField('beer')

Note: As the [documentation from pint](https://pint.readthedocs.io/en/latest/tutorial.html#using-pint-in-your-projects)
states quite clearly: For each project there should be only one unit registry.
Please note that if you change the unit registry for an already created project with
data in a database, you could invalidate your data! So be sure you know what you are
doing!
Still only adding units should be okay.

## Development

### Preparation

You need to install all Python Version that django-pint is compatible with.
In a *nix environment you best could use [pyenv](https://github.com/pyenv/pyenv) to do so.

Furthermore, you need to install [tox](https://tox.wiki/en/latest/) and [pre-commit](https://pre-commit.com/) to lint and test.

You also need docker as our tests require a postgres database to run.
We don't use SQL lite as some bugs only occurred using a proper database.

I recommend using [pipx](https://pypa.github.io/pipx/) to install them.

1. Install `pipx` (see pipx documentation), i.e. with `python3 -m pip install --user pipx && python3 -m pipx ensurepath`
2. Install `pre-commit` running `pipx install pre-commit`
3. Install `tox`  running `pipx install tox`
4. Install the `tox-docker` plugin `pipx inject tox tox-docker`
5. Fork `django-pint` and clone your fork (see [Tutorial](https://docs.github.com/get-started/quickstart/contributing-to-projects))
6. Change into the repo `cd django-pint`
7. Activate `pre-commit` for the repo running `pre-commit install`
8. Check that all linter run fine with the cloned version by running `pre-commit run --all-files`
9. Check that all tests succeed by running `tox`

**Congratulation** you successfully cloned and tested the upstream version of `django-pint`.

Now you can work on your feature branch and test your changes using `tox`.
Your code will be automatically linted and formatted by `pre-commit` if you commit your changes.
If it fails, simply add all changes and try again.
If this doesn't help look at the output of your `git commit` command.

Once you are done, [create a pull request](https://docs.github.com/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork).

### Local development environment with Docker

To run a local development environment with Docker you need to run the following steps:
This is helpful if you have troubles installing `postgresql` or `psycopg2-binary`.

1. `git clone` your fork
2. run `cp .env.example .env`
3. edit `.env` file and change it with your credentials ( the postgres host should match the service name in docker-file so you can use "postgres" )
4. run `cp tests/local.py.docker-example tests/local.py`
5. run `docker-compose up` in the root folder, this should build and start 2 containers, one for postgres and the other one python dependencies. Note you have to be in the [docker](https://stackoverflow.com/a/47078951/3813064) group for this to work.
6. open a new terminal and run `docker-compose exec app bash`, this should open a ssh console in the docker container
7. you can run `pytest` inside the container to see the result of the tests.

### Updating the package
[Python](https://endoflife.date/python) and [Django](https://endoflife.date/django) major versions have defined EOL.
To reduce the maintenance burden and encourage users to use version still receiving security updates any `django-pint` update should match all and only these version of Python and Django that are supported.
Updating these dependencies have to be done in multiple places:
 - `README.md`: Describing it to end users
 - `tox.ini`: For local testing
 - `setup.cfg`: For usage with pip and displaying it in PyPa
 - `.github/workflows/test.yaml`: For the CI/CD Definition
