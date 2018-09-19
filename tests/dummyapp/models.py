from pint import UnitRegistry
from quantityfield.fields import QuantityField, IntegerQuantityField, BigIntegerQuantityField
from django.db import models
from django.utils.six import python_2_unicode_compatible

custom_ureg = UnitRegistry()
custom_ureg.define('custom = [custom]')
custom_ureg.define('kilocustom = 1000 * custom')

@python_2_unicode_compatible
class HayBale(models.Model):
	name = models.CharField(max_length=20)
	weight = QuantityField('gram')
	weight_int = IntegerQuantityField('gram', blank=True, null=True)
	weight_bigint = BigIntegerQuantityField('gram', blank=True, null=True)

	def __str__(self):
		return self.name

@python_2_unicode_compatible
class EmptyHayBale(models.Model):
	name = models.CharField(max_length=20)
	weight = QuantityField('gram', null=True)

	def __str__(self):
		return self.name

@python_2_unicode_compatible
class CustomUregHayBale(models.Model):
	custom = QuantityField('custom', ureg=custom_ureg, null=True)

	def __str__(self):
		return self.name

