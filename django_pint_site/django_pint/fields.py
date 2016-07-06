from pint import Quantity, UnitRegistry

from django.db import models

from . import ureg


def parse_quantity(value):
	quantity, units = value.split(',')
	return ureg('%(quantity)s * %(units)s' % locals())



class QuantityField(models.CharField):
	"""A Django Model Field that resolves to a pint Quantity object"""
	def __init__(self, base_units=None, *args, **kwargs):
		if not base_units:
			raise ValueError('QuantityField must be defined with base units, eg: "gram"')

		# we do this as a way of raising an exception if some crazy unit was supplied.
		unit = getattr(ureg, base_units)

		# if we've not hit an exception here, we should be all good
		self.base_units = base_units

		kwargs['max_length'] = 120
		super(QuantityField, self).__init__(self, *args, **kwargs)

	def deconstruct(self):
		name, path, args, kwargs = super(QuantityField, self).deconstruct()
		kwargs['base_units'] = self.base_units
		kwargs['max_length'] = 120
		return name, path, args, kwargs

	def get_prep_value(self, value):
		return "%d,%s" % (value.magnitude, value.units)

	def from_db_value(self, value, expression, connection, context):
		if value is None:
			return value
		return parse_quantity(value)

	def to_python(self, value):
		if isinstance(value, Quantity):
			return value

		if value is None:
			return None

		return parse_quantity(value)


		