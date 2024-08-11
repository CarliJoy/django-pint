from django.test import TestCase

from pint import Context, DimensionalityError

import quantityfield.fields as fields
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


class TestEdgeCases(TestCase):
    def test_fix_unit_registry(self):
        field = fields.IntegerQuantityField("meter")
        with self.assertRaises(ValueError):
            field.fix_unit_registry(1)

    def test_get_prep_value(self):
        field = fields.IntegerQuantityField("meter")
        with self.assertRaises(ValueError):
            field.get_prep_value("foobar")


class TestContextHandling(TestCase):
    def setUp(self):
        # Define a context where weight is equated to force
        self.context = Context("earth")
        self.context.add_transformation(
            "[mass]", "[force]", lambda ureg, x: x * ureg.gravity
        )
        self.context.add_transformation(
            "[force]", "[mass]", lambda ureg, x: x / ureg.gravity
        )
        ureg.add_context(self.context)

    def test_context_global(self):
        # Activate context globally and test
        ureg.enable_contexts("earth")
        helper.check_matching_unit_dimension(ureg, "kg", ["newton", "kN", "ton"])
        ureg.disable_contexts()

    def test_context_with_block(self):
        # Use context with the 'with' statement
        with ureg.context("earth"):
            helper.check_matching_unit_dimension(ureg, "kg", ["newton", "kN", "ton"])

    def test_invalid_context(self):
        with self.assertRaises(DimensionalityError):
            helper.check_matching_unit_dimension(ureg, "kg", ["newton", "kN", "ton"])

    def test_field_w_context_global(self):
        ureg.enable_contexts("earth")
        self.field = fields.IntegerQuantityField(
            base_units="kg", unit_choices=["newton", "kN", "ton"]
        )
        ureg.disable_contexts()

    def test_field_w_context_block(self):
        with ureg.context("earth"):
            self.field = fields.IntegerQuantityField(
                base_units="kg", unit_choices=["newton", "kN", "ton"]
            )

    def test_invalid_field_wo_context(self):
        with self.assertRaises(DimensionalityError):
            self.field = fields.IntegerQuantityField(
                base_units="kg", unit_choices=["newton", "kN", "ton"]
            )

    def tearDown(self):
        # Clean up by disabling and removing the context
        ureg.disable_contexts()
        ureg.remove_context("earth")
