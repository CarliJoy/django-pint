=====
Usage
=====

This page contains runnable examples of the ``django-pint`` API. All examples
are automatically tested using :mod:`sphinx.ext.doctest`.


Simple Example
--------------

First, define a model with a :class:`~quantityfield.fields.QuantityField`:

.. code-block:: python

   # app/models.py

   from django.db import models
   from quantityfield.fields import QuantityField

   class HayBale(models.Model):
       weight = QuantityField('tonne')

Quantities are stored as float (Django :class:`~django.db.models.FloatField`) and
retrieved like any other field:

.. testsetup:: simple-example

   HayBale.objects.all().delete()

.. doctest:: simple-example

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

If your base unit is atomic (i.e. can be represented by an integer), you may also
use :class:`~quantityfield.fields.IntegerQuantityField` and
:class:`~quantityfield.fields.BigIntegerQuantityField`.

If you prefer exact units you can use the
:class:`~quantityfield.fields.DecimalQuantityField`.

You can also pass :class:`~pint.Quantity` objects to be stored in models. These
are automatically converted to the units defined for the field (but can be
converted to something else when retrieved of course):

.. testsetup:: quantity-objects

   HayBale.objects.all().delete()

.. doctest:: quantity-objects

   >>> from quantityfield.units import ureg
   >>> Quantity = ureg.Quantity
   >>> pounds = Quantity(500 * ureg.pound)
   >>> bale = HayBale.objects.create(weight=pounds)
   >>> bale = HayBale.objects.last()
   >>> bale.weight  # doctest: +ELLIPSIS
   <Quantity(0.2267..., 'metric_ton')>

For comparative lookups, query values will be coerced into the correct units
when comparing values, this means that comparing 1 ounce to 1 tonne should
yield the correct results:

.. testsetup:: filter-example

   HayBale.objects.all().delete()

.. doctest:: filter-example

   >>> from quantityfield.units import ureg
   >>> Quantity = ureg.Quantity
   >>> bale = HayBale.objects.create(weight=0.3)
   >>> less_than_a_tonne = HayBale.objects.filter(weight__lt=Quantity(2000 * ureg.pound))
   >>> less_than_a_tonne.count()
   1


Form Field
----------

Use the inbuilt form field and widget to allow input of quantity values in
different units:

.. code-block:: python

   from django import forms
   from quantityfield.fields import QuantityFormField

   class HayBaleForm(forms.Form):
       weight = QuantityFormField(base_units='gram', unit_choices=['gram', 'ounce', 'milligram'])

The form will render a float input and a select widget to choose the units.
Whenever ``cleaned_data`` is presented from the above form, the weight field
value will be a :class:`~pint.Quantity` with the units set to grams (values are
converted from the units input by the user).

You also can add the ``unit_choices`` directly to the ``ModelField``. It will be
propagated correctly.

.. doctest:: form-example

   >>> from django import forms
   >>> from quantityfield.fields import QuantityFormField
   >>>
   >>> class HayBaleForm(forms.Form):
   ...     weight = QuantityFormField(base_units='gram', unit_choices=['gram', 'ounce', 'milligram'])
   >>>
   >>> form = HayBaleForm(data={'weight_0': '100', 'weight_1': 'gram'})
   >>> form.is_valid()
   True
   >>> form.cleaned_data['weight']
   <Quantity(100.0, 'gram')>


Custom Unit Registry
--------------------

You can also use a custom Pint unit registry in your project ``settings.py``:

.. code-block:: python

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

.. note::

   As the `pint documentation`_ states quite clearly: For each project there
   should be only one unit registry. Please note that if you change the unit
   registry for an already created project with data in a database, you could
   invalidate your data! So be sure you know what you are doing!
   Still only adding units should be okay.

.. _pint documentation: https://pint.readthedocs.io/en/latest/getting/tutorial.html#using-pint-in-your-projects
