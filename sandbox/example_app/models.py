from __future__ import unicode_literals

from django.db import models
from quantityfield.fields import QuantityField
from django.utils.six import python_2_unicode_compatible

# Create your models here.


@python_2_unicode_compatible
class Megalith(models.Model):
	"""A very big stone"""

	stone_type = models.CharField(max_length=20, default="Granite")
	weight = QuantityField('tonnes')

	def __str__(self):
		return 'A {} megalith weighing {}'.format(
			self.stone_type, self.weight
		)



