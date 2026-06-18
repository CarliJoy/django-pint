import warnings
from numbers import Number

from django.forms.widgets import MultiWidget, NumberInput, Select

import pint

from .units import ureg


class QuantityWidget(MultiWidget):
    def __init__(
        self, *, attrs=None, base_units=None, unit_choices=None, allowed_types=None
    ):
        if allowed_types is not None and unit_choices is not None:
            raise TypeError(
                "QuantityWidget received both 'unit_choices' and 'allowed_types'. "
                "Please use 'unit_choices' only."
            )
        if allowed_types is not None:
            warnings.warn(
                "The 'allowed_types' argument is deprecated. Use 'unit_choices' instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            unit_choices = allowed_types
        self.ureg = ureg
        choices = self.get_choices(unit_choices)
        self.base_units = base_units
        attrs = attrs or {}
        attrs.setdefault("step", "any")
        widgets = (NumberInput(attrs=attrs), Select(attrs=attrs, choices=choices))
        super().__init__(widgets, attrs)

    def get_choices(self, unit_choices=None):
        unit_choices = unit_choices or dir(self.ureg)
        return [(x, x) for x in unit_choices]

    def decompress(self, value):
        """This function is called during rendering

        It is responsible to split values for the two widgets
        """
        if isinstance(value, Number):
            # We assume that the given value is a proper number,
            # ready to be rendered
            return [value, self.base_units]
        elif isinstance(value, pint.Quantity):
            return [value.magnitude, value.units]

        return [None, self.base_units]
