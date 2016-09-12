
[![Build Status](https://travis-ci.org/bharling/django-pint.svg?branch=master)](https://travis-ci.org/bharling/django-pint)
[![Coverage Status](https://coveralls.io/repos/github/bharling/django-pint/badge.svg?branch=master)](https://coveralls.io/github/bharling/django-pint?branch=master)

Django Quantity Field
================

A Small django field extension allowing you to store quantities in certain units and perform conversions easily. Uses [pint](https://github.com/hgrecco/pint) behind the scenes.

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
