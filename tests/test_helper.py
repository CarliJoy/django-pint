from django.test import TestCase

from pint import DimensionalityError

import quantityfield.helper as helper
from quantityfield.units import ureg


class TestMatchingUnitDimensionsHelper(TestCase):
    def test_valid_choices(self):
        helper.check_matching_unit_dimension(ureg, "meter", ["mile", "foot", "cm"])

    def test_invalid_choices(self):
        with self.assertRaises(DimensionalityError):
            helper.check_matching_unit_dimension(
                ureg, "meter", ["mile", "foot", "cm", "kg"]
            )
