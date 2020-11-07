from __future__ import unicode_literals

from django.db import models
from quantityfield.fields import QuantityField


# Create your models here.


class Megalith(models.Model):
	"""A very big stone"""

	stone_type = models.CharField(max_length=20, default="Granite")
	weight = QuantityField('tonnes')

	def __str__(self):
		return 'A {} megalith weighing {}'.format(
			self.stone_type, self.weight
		)



