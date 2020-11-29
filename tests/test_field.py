import pytest

from django.core.serializers import serialize
from django.db import transaction
from django.test import TestCase

import json
import warnings
from pint import DimensionalityError, UndefinedUnitError, UnitRegistry

from quantityfield.fields import QuantityField
from quantityfield.units import ureg
from tests.dummyapp.models import CustomUregHayBale, EmptyHayBale, HayBale

Quantity = ureg.Quantity


class TestFieldCreate(TestCase):
    def test_sets_units(self):
        test_grams = QuantityField("gram")
        self.assertEqual(test_grams.units, ureg.gram)

    def test_fails_with_unknown_units(self):
        with self.assertRaises(UndefinedUnitError):
            test_crazy_units = QuantityField("zinghie")  # noqa: F841

    def test_base_units_is_required(self):
        with self.assertRaises(TypeError):
            no_units = QuantityField()  # noqa: F841

    def test_base_units_set_with_name(self):
        okay_units = QuantityField(base_units="meter")  # noqa: F841

    def test_base_units_are_invalid(self):
        with self.assertRaises(ValueError):
            wrong_units = QuantityField(None)  # noqa: F841

    def test_unit_choices_must_be_valid_units(self):
        with self.assertRaises(UndefinedUnitError):
            QuantityField(base_units="mile", unit_choices=["gunzu"])

    def test_unit_choices_must_match_base_dimensionality(self):
        with self.assertRaises(DimensionalityError):
            QuantityField(base_units="gram", unit_choices=["meter", "ounces"])


@pytest.mark.django_db
class TestFieldSave(TestCase):
    def setUp(self):
        HayBale.objects.create(
            weight=100, weight_int=100, weight_bigint=100, name="grams"
        )
        HayBale.objects.create(weight=Quantity(10 * ureg.ounce), name="ounce")
        self.lightest = HayBale.objects.create(weight=1, name="lightest")
        self.heaviest = HayBale.objects.create(weight=1000, name="heaviest")
        EmptyHayBale.objects.create(name="Empty")
        CustomUregHayBale.objects.create(custom=5)
        CustomUregHayBale.objects.create(custom=5 * ureg.kilocustom)

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

    def test_accepts_auto_null(self):
        empty = EmptyHayBale.objects.first()
        self.assertIsNone(empty.weight, None)

    def test_accepts_assigned_null(self):
        new = EmptyHayBale()
        new.weight = None
        new.name = "Test"
        new.save()
        self.assertIsNone(new.weight)

    def test_accepts_assigned_float(self):
        new = EmptyHayBale(name="FloatTest")
        new.weight = 707
        new.save()
        obj: EmptyHayBale = EmptyHayBale.objects.last()
        self.assertEqual(obj.name, "FloatTest")
        self.assertEqual(obj.weight.units, "gram")
        self.assertEqual(obj.weight.magnitude, 707)

    def test_accepts_default_pint_unit(self):
        new = EmptyHayBale(name="DefaultPintUnitTest")
        units = UnitRegistry()
        new.weight = 5 * units.kilogram
        # Different Registers so we expect a warning!
        with self.assertWarns(RuntimeWarning):
            new.save()
        obj: EmptyHayBale = EmptyHayBale.objects.last()
        self.assertEqual(obj.name, "DefaultPintUnitTest")
        self.assertEqual(obj.weight.units, "gram")
        self.assertEqual(obj.weight.magnitude, 5000)

    def test_accepts_default_app_unit(self):
        new = EmptyHayBale(name="DefaultAppUnitTest")
        new.weight = 5 * ureg.kilogram
        # Make sure that the correct argument does not raise a warning
        with warnings.catch_warnings(record=True) as w:
            new.save()
        assert len(w) == 0
        obj: EmptyHayBale = EmptyHayBale.objects.last()
        self.assertEqual(obj.name, "DefaultAppUnitTest")
        self.assertEqual(obj.weight.units, "gram")
        self.assertEqual(obj.weight.magnitude, 5000)

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

    def tearDown(self):
        HayBale.objects.all().delete()
        EmptyHayBale.objects.all().delete()

    def test_custom_ureg(self):
        obj = CustomUregHayBale.objects.first()
        self.assertIsInstance(obj.custom, ureg.Quantity)
        self.assertEqual(str(obj.custom), "5.0 custom")

        obj = CustomUregHayBale.objects.last()
        self.assertEqual(str(obj.custom), "5000.0 custom")

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
