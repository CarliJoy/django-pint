
[![Build Status](https://travis-ci.org/bharling/django-pint.svg?branch=master)](https://travis-ci.org/bharling/django-pint)
[![Coverage Status](https://coveralls.io/repos/github/bharling/django-pint/badge.svg?branch=master)](https://coveralls.io/github/bharling/django-pint?branch=master)
[![PyPi version](https://pypip.in/v/$REPO/badge.png)](https://crate.io/packages/$REPO/)
[![PyPi downloads](https://pypip.in/d/$REPO/badge.png)](https://crate.io/packages/$REPO/)

Django Quantity Field
================

A Small django field extension allowing you to store quantities in certain units and perform conversions easily. Uses [pint](https://github.com/hgrecco/pint) behind the scenes. Also contains a form field class and form widget that allows a user to choose alternative units to input data. The cleaned_data will output the value in the base_units defined for the field, eg: you specify you want to store a value in grams but will allow users to input either grams or ounces.

Compatibility
-------------

Requires django >= 1.8, and python 2.7/3.2/3.3/3.4

Installation
------------

    pip install django-pint


Simple Example
-----------------------
Best way to illustrate is with an example

    # app/models.py
    
    from django.db import models
    from quantityfield.fields import QuantityField
    
    class HayBale(models.Model):
	    weight = QuantityField('tonne')

Quantities are stored and retrieved like any other field

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

You can also pass Quantity objects to be stored in models. These are automatically converted to the units defined for the field ( but can be converted to something else when retrieved of course ).

    >> from quantityfield import ureg
    >> Quantity = ureg.Quantity
    >> pounds = Quantity(500 * ureg.pound)
    >> bale = HayBale.objects.create(weight=pounds)
    >> bale.weight
    <Quantity(0.226796, 'tonne')>

Use the inbuilt form field and widget to allow input of quantity values in different units

    from quantityfield.fields import QuantityFormField

    class HayBaleForm(forms.Form):
        weight = QuantityFormField(base_units='gram', unit_choices=['gram', 'ounce', 'milligram'])

The form will render a float input and a select widget to choose the units. Whenever cleaned_data is presented from the above form the weight field value will be a Quantity with the units set to grams ( values are converted from the units input by the user ).
