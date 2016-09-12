from quantityfield.fields import QuantityField
from django.db import models


class HayBale(models.Model):
	name = models.CharField(max_length=20)
	weight = QuantityField('gram')

