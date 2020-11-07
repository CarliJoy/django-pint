from django.test import TestCase

from quantityfield.fields import (
    QuantityField,
    QuantityFormField,
    IntegerQuantityFormField,
)
from quantityfield.widgets import QuantityWidget


from quantityfield import ureg

Quantity = ureg.Quantity

from django.db import transaction

from tests.dummyapp.models import HayBale, EmptyHayBale

from django import forms

from pint import DimensionalityError, UndefinedUnitError


class HayBaleForm(forms.ModelForm):
    weight = QuantityFormField(base_units="gram", unit_choices=["ounce", "gram"])
    weight_int = IntegerQuantityFormField(
        base_units="gram", unit_choices=["ounce", "gram"]
    )

    class Meta:
        model = HayBale
        exclude = ["weight_bigint"]


class NullableWeightForm(forms.Form):
    weight = QuantityFormField(base_units="gram", required=False)


class UnitChoicesForm(forms.Form):
    distance = QuantityFormField(
        base_units="kilometer", unit_choices=["mile", "kilometer", "yard", "feet"]
    )


class TestWidgets(TestCase):
    def test_creates_correct_widget_for_modelform(self):
        form = HayBaleForm()
        self.assertIsInstance(form.fields["weight"], QuantityFormField)
        self.assertIsInstance(form.fields["weight"].widget, QuantityWidget)

    def test_displays_initial_data_correctly(self):
        form = HayBaleForm(
            initial={"weight": Quantity(100 * ureg.gram), "name": "test"}
        )

    def test_clean_yields_quantity(self):
        form = HayBaleForm(
            data={
                "weight_0": 100.0,
                "weight_1": "gram",
                "weight_int_0": 100,
                "weight_int_1": "gram",
                "name": "test",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertIsInstance(form.cleaned_data["weight"], Quantity)

    def test_clean_yields_quantity_in_correct_units(self):
        form = HayBaleForm(
            data={
                "weight_0": 1.0,
                "weight_1": "ounce",
                "weight_int_0": 1,
                "weight_int_1": "ounce",
                "name": "test",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(str(form.cleaned_data["weight"].units), "gram")
        self.assertAlmostEqual(form.cleaned_data["weight"].magnitude, 28.349523125)

    def test_base_units_is_required_for_form_field(self):
        with self.assertRaises(ValueError):
            field = QuantityFormField()

    def test_quantityfield_can_be_null(self):
        form = NullableWeightForm(data={"weight_0": None, "weight_1": None})
        self.assertTrue(form.is_valid())

    def test_validate_units(self):
        form = UnitChoicesForm(data={"distance_0": 100, "distance_1": "ounce"})
        self.assertFalse(form.is_valid())

    def test_base_units_is_included_by_default(self):
        field = QuantityFormField(base_units="mile", unit_choices=["meters", "feet"])
        self.assertIn("mile", field.units)

    def test_form_field_displays_unit_choices(self):
        form = UnitChoicesForm()
        self.assertListEqual(
            [
                ("mile", "mile"),
                ("kilometer", "kilometer"),
                ("yard", "yard"),
                ("feet", "feet"),
            ],
            form.fields["distance"].widget.widgets[1].choices,
        )

    def test_unit_choices_must_be_valid_units(self):
        with self.assertRaises(UndefinedUnitError):
            field = QuantityFormField(base_units="mile", unit_choices=["gunzu"])

    def test_unit_choices_must_match_base_dimensionality(self):
        with self.assertRaises(DimensionalityError):
            field = QuantityFormField(
                base_units="gram", unit_choices=["meter", "ounces"]
            )

    def test_widget_display(self):
        bale = HayBale.objects.create(name="Fritz", weight=20)
        form = HayBaleForm(instance=bale)
        html = str(form)
        self.assertIn(
            '<input type="number" name="weight_int_0" step="any" required id="id_weight_int_0">',
            html,
        )

        self.assertIn('<option value="ounce">ounce</option>', html)
