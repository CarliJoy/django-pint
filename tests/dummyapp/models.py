from quantityfield.fields import QuantityField
from django.db import models
from django.utils.six import python_2_unicode_compatible

@python_2_unicode_compatible
class HayBale(models.Model):
	name = models.CharField(max_length=20)
	weight = QuantityField('gram')

	def __str__(self):
		return self.name

@python_2_unicode_compatible
class EmptyHayBale(models.Model):
	name = models.CharField(max_length=20)
	weight = QuantityField('gram', null=True)

	def __str__(self):
		return self.name

