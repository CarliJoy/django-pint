from django.db import models

from quantityfield.fields import (
    BigIntegerQuantityField,
    IntegerQuantityField,
    QuantityField,
)


class HayBale(models.Model):
    name = models.CharField(max_length=20)
    weight = QuantityField("gram")
    weight_int = IntegerQuantityField("gram", blank=True, null=True)
    weight_bigint = BigIntegerQuantityField("gram", blank=True, null=True)


class EmptyHayBaleFloat(models.Model):
    name = models.CharField(max_length=20)
    weight = QuantityField("gram", null=True)


class EmptyHayBaleInt(models.Model):
    name = models.CharField(max_length=20)
    weight = IntegerQuantityField("gram", null=True)


class EmptyHayBaleBigInt(models.Model):
    name = models.CharField(max_length=20)
    weight = BigIntegerQuantityField("gram", null=True)


class CustomUregHayBale(models.Model):
    # Custom is defined in settings in conftest.py
    custom = QuantityField("custom")
    custom_int = IntegerQuantityField("custom")
    custom_bigint = BigIntegerQuantityField("custom")


class ChoicesDefinedInModel(models.Model):
    weight = QuantityField("kilogram", unit_choices=["milligram", "pounds"])


class ChoicesDefinedInModelInt(models.Model):
    weight = IntegerQuantityField("kilogram", unit_choices=["milligram", "pounds"])
