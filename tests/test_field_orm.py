from decimal import Decimal

import pytest

from django.db.models import Min, Subquery
from django.test import TestCase

from quantityfield.units import ureg
from tests.dummyapp.models import (
    BigIntFieldSaveModel,
    EmptyHayBalePositiveInt,
    FloatFieldSaveModel,
    IntFieldSaveModel,
    DecimalFieldSaveModel,
)

Quantity = ureg.Quantity


class BaseMixinQuantityFieldORM:
    """Base mixin for ORM tests for QuantityField types."""
    MODEL: type
    FIELD_NAME: str = "weight"
    CREATE_KWARGS_LIGHT: dict = {"name": "light", FIELD_NAME: 100}
    CREATE_KWARGS_HEAVY: dict = {"name": "heavy", FIELD_NAME: 200}
    EXPECTED_TYPE: type

    def setUp(self):
        self.light = self.MODEL.objects.create(**self.CREATE_KWARGS_LIGHT)
        self.heavy = self.MODEL.objects.create(**self.CREATE_KWARGS_HEAVY)

    def tearDown(self):
        self.MODEL.objects.all().delete()

    def test_bulk_update_with_subquery(self):
        min_value_qs = self.MODEL.objects.annotate(
            min_value=Min(self.FIELD_NAME)
        ).values("min_value")[:1]

        self.MODEL.objects.all().update(**{self.FIELD_NAME: Subquery(min_value_qs)})

        self.light.refresh_from_db()
        self.heavy.refresh_from_db()

        self.assertEqual(Quantity(self.EXPECTED_TYPE(100) * ureg.gram), getattr(self.light, self.FIELD_NAME))
        self.assertEqual(Quantity(self.EXPECTED_TYPE(100) * ureg.gram), getattr(self.heavy, self.FIELD_NAME))


@pytest.mark.django_db
class TestDecimalQuantityFieldORM(BaseMixinQuantityFieldORM, TestCase):
    MODEL = DecimalFieldSaveModel
    EXPECTED_TYPE = Decimal


@pytest.mark.django_db
class TestFloatQuantityFieldORM(BaseMixinQuantityFieldORM, TestCase):
    MODEL = FloatFieldSaveModel
    EXPECTED_TYPE = float


@pytest.mark.django_db
class TestIntegerQuantityFieldORM(BaseMixinQuantityFieldORM, TestCase):
    MODEL = IntFieldSaveModel
    EXPECTED_TYPE = int


@pytest.mark.django_db
class TestBigIntegerQuantityFieldORM(BaseMixinQuantityFieldORM, TestCase):
    MODEL = BigIntFieldSaveModel
    EXPECTED_TYPE = int


@pytest.mark.django_db
class TestPositiveIntegerQuantityFieldORM(BaseMixinQuantityFieldORM, TestCase):
    MODEL = EmptyHayBalePositiveInt
    EXPECTED_TYPE = int
