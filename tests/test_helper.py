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
    """Class to test ureg.context for compatible units as described in issue #99.
    pint allows users to define a special context for unit conversions,
    e.g. on earth a mass can directly be converted to a force given the
    acceleration 'constant' on earth.
    We will test the unit compatibility via the helper function for both
    both context activated globally via ureg and within a with block. Finally
    test the conversion integrated inside an IntegerQuantityField. Also the
    negatives are tested: without the context, mass should not be accepted
    as a matching unit for force.
    """

    def setUp(self):
        """Setup a pint context in the UnitRegistry."""
        # Define a context where mass is equated to force via earth's
        # standard acceleration of gravity and vice versa
        # (https://en.wikipedia.org/wiki/Standard_gravity)
        self.context = Context("earth")
        # mass -> force
        self.context.add_transformation(
            "[mass]", "[force]", lambda ureg, x: x * ureg.gravity
        )
        # force -> mass
        self.context.add_transformation(
            "[force]", "[mass]", lambda ureg, x: x / ureg.gravity
        )
        ureg.add_context(self.context)

    def test_context_global(self):
        """Activate ureg.context globally and test conversion compatibility directly."""
        # Activate context globally and test
        ureg.enable_contexts("earth")
        helper.check_matching_unit_dimension(ureg, "kg", ["newton", "kN", "ton"])
        ureg.disable_contexts()

    def test_context_with_block(self):
        """Activate ureg.context in with block and test conversion compatibility
        directly."""
        # Use context with the 'with' statement
        with ureg.context("earth"):
            helper.check_matching_unit_dimension(ureg, "kg", ["newton", "kN", "ton"])

    def test_invalid_context(self):
        """Negative test: Conversion mass to force should fail without context."""
        with self.assertRaises(DimensionalityError):
            helper.check_matching_unit_dimension(ureg, "kg", ["newton", "kN", "ton"])

    def test_field_w_context_global(self):
        """Negative test: Conversion mass to force should fail without context."""
        ureg.enable_contexts("earth")
        self.field = fields.IntegerQuantityField(
            base_units="kg", unit_choices=["newton", "kN", "ton"]
        )
        ureg.disable_contexts()

    def test_field_w_context_block(self):
        """Activate ureg.context globally and test conversion compatibility complete
        Field."""
        with ureg.context("earth"):
            self.field = fields.IntegerQuantityField(
                base_units="kg", unit_choices=["newton", "kN", "ton"]
            )

    def test_invalid_field_wo_context(self):
        """Negative test: Conversion mass to force should fail without context."""
        with self.assertRaises(DimensionalityError):
            self.field = fields.IntegerQuantityField(
                base_units="kg", unit_choices=["newton", "kN", "ton"]
            )

    def tearDown(self):
        """Disable and remove the contexts to not interfere with other tests."""
        # Clean up by disabling and removing the context
        ureg.disable_contexts()
        ureg.remove_context("earth")
