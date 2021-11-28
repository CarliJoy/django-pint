
[![Build Status](https://api.travis-ci.com/CarliJoy/django-pint.svg?branch=master)](https://travis-ci.com/github/CarliJoy/django-pint)
[![codecov](https://codecov.io/gh/CarliJoy/django-pint/branch/master/graph/badge.svg?token=I3M4CLILXE)](https://codecov.io/gh/CarliJoy/django-pint)
[![PyPI Downloads](https://img.shields.io/pypi/dm/django-pint.svg?maxAge=2592000?style=plastic)](https://pypistats.org/packages/django-pint)
[![Python Versions](https://img.shields.io/pypi/pyversions/django-pint.svg)](https://pypi.org/project/django-pint/)
[![PyPI Version](https://img.shields.io/pypi/v/django-pint.svg?maxAge=2592000?style=plastic)](https://pypi.org/project/django-pint/)
[![Project Status](https://img.shields.io/pypi/status/django-pint.svg)](https://pypi.org/project/SyncGitlab2MSProject/)
[![Wheel Build](https://img.shields.io/pypi/wheel/django-pint.svg)](https://pypi.org/project/django-pint/)
[![Code Style Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/django-pint/badge/?version=latest)](https://django-pint.readthedocs.io/en/latest/?badge=latest)

# Django Quantity Field


A Small django field extension allowing you to store quantities in certain units and perform conversions easily. Uses [pint](https://github.com/hgrecco/pint) behind the scenes. Also contains a form field class and form widget that allows a user to choose alternative units to input data. The cleaned_data will output the value in the base_units defined for the field, eg: you specify you want to store a value in grams but will allow users to input either grams or ounces.

## Compatibility


Requires django >= 2.2, and python 3.6/3.7/3.8/3.9/3.10

Test with the following combinations:
* Django 2.2 (Python 3.6, 3.7, 3.8)
* Django 3.0 (Python 3.6, 3.7, 3.8)
* Django 3.1 (Python 3.6, 3.7, 3.8, 3.9)
* Django 3.2 (Python 3.6, 3.7, 3.8, 3.9, 3.10)

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
Quantity with the units set to grams (values are converted from the units input by the user ).
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

## Set Up Local Testing
As SQL Lite is not very strict in handling types we use Postgres for testing.
This will bring up some possible pitfalls using proper databases.
To get the test running please install `postgresql` on your OS.
You need to have `psycopg2-binary` installed (see `tox.ini` for further requirements)
and a user with the proper permissions set. See `ci_setup_postgres.sh`
for an example on HowTo set it up. Or simply run:
`sudo -u postgres ./ci_setup_postgres.sh`.

You can also use you local credentials by creating a `tests/local.py` file.
See `test/settings.py` for a description.


## Local development environment with Docker

To run a local development environment with Docker you need to run the following steps:
This is helpful if you have troubles installing `postgresql` or `psycopg2-binary`.

1. `git clone` your fork
2. run `cp .env.example .env`
3. edit `.env` file and change it with your credentials ( the postgres host should match the service name in docker-file so you can use "postgres" )
4. run `cp tests/local.py.docker-example tests/local.py`
5. run `docker-compose up` in the root folder, this should build and start 2 containers, one for postgres and the other one python dependencies. Note you have to be in the [docker](https://stackoverflow.com/a/47078951/3813064) group for this to work.
6. open a new terminal and run `docker-compose exec app bash`, this should open a ssh console in the docker container
7. you can run `pytest` inside the container to see the result of the tests.
