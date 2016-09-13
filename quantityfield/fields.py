

from django.db import models

from django import forms

from . import ureg

Quantity = ureg.Quantity

from .widgets import QuantityWidget

from django.utils.six import python_2_unicode_compatible

from django.core.exceptions import ValidationError

from pint import DimensionalityError, UndefinedUnitError

class QuantityField(models.FloatField):
	"""A Django Model Field that resolves to a pint Quantity object"""
	def __init__(self, base_units=None, *args, **kwargs):
		if not base_units:
			raise ValueError('QuantityField must be defined with base units, eg: "gram"')

		# we do this as a way of raising an exception if some crazy unit was supplied.
		unit = getattr(ureg, base_units)

		# if we've not hit an exception here, we should be all good
		self.base_units = base_units
		super(QuantityField, self).__init__(*args, **kwargs)

	@property
	def units(self):
		return self.base_units

	def deconstruct(self):
		name, path, args, kwargs = super(QuantityField, self).deconstruct()
		kwargs['base_units'] = self.base_units
		return name, path, args, kwargs

	def get_prep_value(self, value):
		# we store the value in the base units defined for this field
		if value==None:
			return None

		if isinstance(value, Quantity):
			to_save = value.to(self.base_units)
			return float(to_save.magnitude)
		return value

	def value_to_string(self, obj):
		value = self.value_from_object(obj)
		return self.get_prep_value(value)

	def from_db_value(self, value, expression, connection, context):
		if value is None:
			return value
		return Quantity(value * getattr(ureg, self.base_units))

	def to_python(self, value):
		if isinstance(value, Quantity):
			return value

		if value is None:
			return None

		return Quantity(value * getattr(ureg, self.base_units))

	def get_prep_lookup(self, lookup_type, value):

		if lookup_type in ['lt', 'gt', 'lte', 'gte']:
			if isinstance(value, Quantity):
				v = value.to(self.base_units)
				return v.magnitude
			return value

	def formfield(self, **kwargs):
		defaults = {'form_class':QuantityFormField, 'base_units':self.base_units}
		defaults.update(kwargs)
		return super(QuantityField, self).formfield(**defaults)


class QuantityFormField(forms.FloatField):
	"""This formfield allows a user to choose which units they
		wish to use to enter a value, but the value is yielded in
		the base_units
	"""

	def __init__(self, *args, **kwargs):
		self.base_units = kwargs.pop('base_units', None)
		if not self.base_units:
			raise ValueError('QuantityFormField requires a base_units kwarg of a single unit type (eg: grams)')
		self.units = kwargs.pop('unit_choices', [self.base_units])
		if self.base_units not in self.units:
			self.units.append(self.base_units)


		base_unit = getattr(ureg, self.base_units)

		for _unit in self.units:
			unit = getattr(ureg, _unit)
			if unit.dimensionality != base_unit.dimensionality:
				raise DimensionalityError(base_unit, unit)



		kwargs.update({'widget': QuantityWidget(allowed_types=self.units)})
		super(QuantityFormField, self).__init__(*args, **kwargs)

	def clean(self, value):
		if isinstance(value, list):
			val = value[0]
			units = value[1]
			if val is None:
				return None
			if not units in self.units:
				raise ValidationError('%(units)s is not a valid choice' % locals())
			q = Quantity(float(val) * getattr(ureg, units))
			return q.to(self.base_units)
		return Quantity(value * getattr(ureg, self.base_units))