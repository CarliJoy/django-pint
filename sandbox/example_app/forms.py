from django import forms

from quantityfield.fields import QuantityFormField


class TestForm(forms.Form):
    """docstring for TestForm"""

    amount = QuantityFormField(base_units="grams", unit_choices=["ounce", "gram"])
