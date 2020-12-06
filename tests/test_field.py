import pytest

from django.core.serializers import serialize
from django.db import transaction
from django.db.models import Field, Model
from django.test import TestCase

import json
import warnings
from pint import DimensionalityError, UndefinedUnitError, UnitRegistry
from typing import Type, Union

from quantityfield.fields import (
    BigIntegerQuantityField,
    IntegerQuantityField,
    QuantityField,
    QuantityFieldMixin,
)
from quantityfield.units import ureg
from tests.dummyapp.models import (
    CustomUregHayBale,
    EmptyHayBaleBigInt,
    EmptyHayBaleFloat,
    EmptyHayBaleInt,
    HayBale,
)

Quantity = ureg.Quantity


class BaseMixinTestFieldCreate:
    FIELD: Type[Union[Field, QuantityFieldMixin]]

    def test_sets_units(self):
        test_grams = self.FIELD("gram")
        self.assertEqual(test_grams.units, ureg.gram)

    def test_fails_with_unknown_units(self):
        with self.assertRaises(UndefinedUnitError):
            test_crazy_units = self.FIELD("zinghie")  # noqa: F841

    def test_base_units_is_required(self):
        with self.assertRaises(TypeError):
            no_units = self.FIELD()  # noqa: F841

    def test_base_units_set_with_name(self):
        okay_units = self.FIELD(base_units="meter")  # noqa: F841

    def test_base_units_are_invalid(self):
        with self.assertRaises(ValueError):
            wrong_units = self.FIELD(None)  # noqa: F841

    def test_unit_choices_must_be_valid_units(self):
        with self.assertRaises(UndefinedUnitError):
            self.FIELD(base_units="mile", unit_choices=["gunzu"])

    def test_unit_choices_must_match_base_dimensionality(self):
        with self.assertRaises(DimensionalityError):
            self.FIELD(base_units="gram", unit_choices=["meter", "ounces"])


class TestFloatFieldCrate(BaseMixinTestFieldCreate, TestCase):
    FIELD = QuantityField


class TestIntegerFieldCreate(BaseMixinTestFieldCreate, TestCase):
    FIELD = IntegerQuantityField


class TestBigIntegerFieldCreate(BaseMixinTestFieldCreate, TestCase):
    FIELD = BigIntegerQuantityField


@pytest.mark.django_db
class TestCustomUreg(TestCase):
    def setUp(self):
        # Custom Values are fined in confest.py
        CustomUregHayBale.objects.create(custom=5, custom_int=5, custom_bigint=5)
        CustomUregHayBale.objects.create(
            custom=5 * ureg.kilocustom,
            custom_int=5 * ureg.kilocustom,
            custom_bigint=5 * ureg.kilocustom,
        )

    def tearDown(self):
        CustomUregHayBale.objects.all().delete()

    def test_custom_ureg_float(self):
        obj = CustomUregHayBale.objects.first()
        self.assertIsInstance(obj.custom, ureg.Quantity)
        self.assertEqual(str(obj.custom), "5.0 custom")

        obj = CustomUregHayBale.objects.last()
        self.assertEqual(str(obj.custom), "5000.0 custom")

    def test_custom_ureg_int(self):
        obj = CustomUregHayBale.objects.first()
        self.assertIsInstance(obj.custom_int, ureg.Quantity)
        self.assertEqual(str(obj.custom_int), "5 custom")

        obj = CustomUregHayBale.objects.last()
        self.assertEqual(str(obj.custom_int), "5000 custom")

    def test_custom_ureg_bigint(self):
        obj = CustomUregHayBale.objects.first()
        self.assertIsInstance(obj.custom_int, ureg.Quantity)
        self.assertEqual(str(obj.custom_bigint), "5 custom")

        obj = CustomUregHayBale.objects.last()
        self.assertEqual(str(obj.custom_bigint), "5000 custom")


class BaseMixinNullAble:
    EMPTY_MODEL: Type[Model]

    def setUp(self):
        self.EMPTY_MODEL.objects.create(name="Empty")

    def tearDown(self) -> None:
        self.EMPTY_MODEL.objects.all().delete()

    def test_accepts_assigned_null(self):
        new = self.EMPTY_MODEL()
        new.weight = None
        new.name = "Test"
        new.save()
        self.assertIsNone(new.weight)
        # Also get it from database to verify
        from_db = self.EMPTY_MODEL.objects.last()
        self.assertIsNone(from_db.weight)

    def test_accepts_auto_null(self):
        empty = self.EMPTY_MODEL.objects.first()
        self.assertIsNone(empty.weight, None)

    def test_accepts_default_pint_unit(self):
        new = self.EMPTY_MODEL(name="DefaultPintUnitTest")
        units = UnitRegistry()
        new.weight = 5 * units.kilogram
        # Different Registers so we expect a warning!
        with self.assertWarns(RuntimeWarning):
            new.save()
        obj = self.EMPTY_MODEL.objects.last()
        self.assertEqual(obj.name, "DefaultPintUnitTest")
        self.assertEqual(obj.weight.units, "gram")
        self.assertEqual(obj.weight.magnitude, 5000)

    def test_accepts_default_app_unit(self):
        new = self.EMPTY_MODEL(name="DefaultAppUnitTest")
        new.weight = 5 * ureg.kilogram
        # Make sure that the correct argument does not raise a warning
        with warnings.catch_warnings(record=True) as w:
            new.save()
        assert len(w) == 0
        obj = self.EMPTY_MODEL.objects.last()
        self.assertEqual(obj.name, "DefaultAppUnitTest")
        self.assertEqual(obj.weight.units, "gram")
        self.assertEqual(obj.weight.magnitude, 5000)

    def test_accepts_assigned_whole_number(self):
        new = self.EMPTY_MODEL(name="WholeNumber")
        new.weight = 707
        new.save()
        obj = self.EMPTY_MODEL.objects.last()
        self.assertEqual(obj.name, "WholeNumber")
        self.assertEqual(obj.weight.units, "gram")
        self.assertEqual(obj.weight.magnitude, 707)

    def test_accepts_assigned_float_number(self):
        new = self.EMPTY_MODEL(name="FloatNumber")
        new.weight = 707.7
        new.save()
        obj = self.EMPTY_MODEL.objects.last()
        self.assertEqual(obj.name, "FloatNumber")
        self.assertEqual(obj.weight.units, "gram")
        # FIXME: This should fail with Int, but it does not!
        #        Probably because we using SQL Lite
        self.assertEqual(obj.weight.magnitude, 707.7)


@pytest.mark.django_db
class TestNullableFloat(BaseMixinNullAble, TestCase):
    EMPTY_MODEL = EmptyHayBaleFloat


@pytest.mark.django_db
class TestNullableInt(BaseMixinNullAble, TestCase):
    EMPTY_MODEL = EmptyHayBaleInt


@pytest.mark.django_db
class TestNullableBigInt(BaseMixinNullAble, TestCase):
    EMPTY_MODEL = EmptyHayBaleBigInt


@pytest.mark.django_db
class TestFieldSave(TestCase):
    def setUp(self):
        HayBale.objects.create(
            weight=100, weight_int=100, weight_bigint=100, name="grams"
        )
        HayBale.objects.create(weight=Quantity(10 * ureg.ounce), name="ounce")
        self.lightest = HayBale.objects.create(weight=1, name="lightest")
        self.heaviest = HayBale.objects.create(weight=1000, name="heaviest")

    def tearDown(self):
        HayBale.objects.all().delete()

    def test_stores_value_in_base_units(self):
        item = HayBale.objects.get(name="ounce")
        self.assertEqual(item.weight.units, "gram")
        self.assertAlmostEqual(item.weight.magnitude, 283.49523125)

    def test_store_integer_loss_of_precision(self):
        with transaction.atomic():
            with self.assertRaisesRegex(ValueError, "loss of precision"):
                HayBale(name="x", weight=0, weight_int=Quantity(10 * ureg.ounce)).save()
        with transaction.atomic():
            with self.assertRaisesRegex(ValueError, "loss of precision"):
                HayBale(
                    name="x", weight=0, weight_bigint=Quantity(10 * ureg.ounce)
                ).save()

    def test_fails_with_incompatible_units(self):
        # we have to wrap this in a transaction
        # fixing a unit test problem
        # http://stackoverflow.com/questions/21458387/transactionmanagementerror-you-cant-execute-queries-until-the-end-of-the-atom
        metres = Quantity(100 * ureg.meter)
        with transaction.atomic():
            with self.assertRaises(DimensionalityError):
                HayBale.objects.create(weight=metres, name="Should Fail")

    def test_value_stored_as_quantity(self):
        obj = HayBale.objects.first()
        self.assertIsInstance(obj.weight, Quantity)
        self.assertEqual(str(obj.weight), "100.0 gram")
        self.assertEqual(str(obj.weight_int), "100 gram")
        self.assertEqual(str(obj.weight_bigint), "100 gram")

    def test_value_conversion(self):
        obj = HayBale.objects.first()
        ounces = obj.weight.to(ureg.ounce)
        self.assertAlmostEqual(ounces.magnitude, 3.52739619496)
        self.assertEqual(ounces.units, ureg.ounce)

    def test_order_by(self):
        qs = HayBale.objects.all().order_by("weight")
        self.assertEqual(qs[0].name, "lightest")

    def test_comparison_with_number(self):
        qs = HayBale.objects.filter(weight__gt=2)
        self.assertNotIn(self.lightest, qs)

    def test_comparison_with_quantity(self):
        weight = Quantity(20 * ureg.gram)
        qs = HayBale.objects.filter(weight__gt=weight)
        self.assertNotIn(self.lightest, qs)

    def test_comparison_with_quantity_respects_units(self):
        # 1 ounce = 28.34 grams
        weight = Quantity(0.8 * ureg.ounce)
        qs = HayBale.objects.filter(weight__gt=weight)
        self.assertNotIn(self.lightest, qs)

    def test_comparison_is_actually_numeric(self):
        qs = HayBale.objects.filter(weight__gt=1.0)
        self.assertNotIn(self.lightest, qs)

    def test_serialisation(self):
        serialized = serialize(
            "json",
            [
                HayBale.objects.first(),
            ],
        )
        deserialized = json.loads(serialized)
        obj = deserialized[0]["fields"]
        self.assertEqual(obj["weight"], "100.0")
        self.assertEqual(obj["weight_int"], "100")
