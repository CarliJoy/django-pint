from django.db import models

from pint import UnitRegistry

from quantityfield.fields import (
    BigIntegerQuantityField,
    IntegerQuantityField,
    QuantityField,
)

custom_ureg = UnitRegistry()
custom_ureg.define("custom = [custom]")
custom_ureg.define("kilocustom = 1000 * custom")


class HayBale(models.Model):
    name = models.CharField(max_length=20)
    weight = QuantityField("gram")
    weight_int = IntegerQuantityField("gram", blank=True, null=True)
    weight_bigint = BigIntegerQuantityField("gram", blank=True, null=True)


class EmptyHayBale(models.Model):
    name = models.CharField(max_length=20)
    weight = QuantityField("gram", null=True)


class CustomUregHayBale(models.Model):
    custom = QuantityField("custom", ureg=custom_ureg, null=True)
