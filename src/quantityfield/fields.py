from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import formats
from django.utils.translation import gettext_lazy as _

import warnings
from pint import Quantity
from typing import List, Optional

from quantityfield.exceptions import PrecisionLoss
from quantityfield.helper import check_matching_unit_dimension

from .units import ureg
from .widgets import QuantityWidget


def safe_to_int(value):
    """
    Check if a value is an int otherwise warn that it can't be converted
    :param value:
    :return:
    """
    float_value = float(value)
    int_value = int(float_value)
    # We round to compensate for possible float rounding errors
    if round(abs(int_value - float_value), 10) == 0:
        return int_value
    else:
        raise PrecisionLoss(
            _("Possible loss of precision converting value to integer: %s") % value
        )


class QuantityFieldMixin(object):
    to_number_type = NotImplemented

    """A Django Model Field that resolves to a pint Quantity object"""

    def __init__(
        self, base_units: str, *args, unit_choices: Optional[List[str]] = None, **kwargs
    ):
        """
        Create a Quantity field
        :param base_units: Unit description of base unit
        :param unit_choices: If given the possible unit choices with the same
                             dimension like the base_unit
        """
        if not isinstance(base_units, str):
            raise ValueError(
                'QuantityField must be defined with base units, eg: "gram"'
            )

        self.ureg = ureg

        # we do this as a way of raising an exception if some crazy unit was supplied.
        unit = getattr(self.ureg, base_units)  # noqa: F841

        # if we've not hit an exception here, we should be all good
        self.base_units = base_units

        if unit_choices is None:
            self.unit_choices: List[str] = [self.base_units]
        else:
            self.unit_choices = unit_choices

        # Check if all unit_choices are valid
        check_matching_unit_dimension(self.ureg, self.base_units, self.unit_choices)

        super(QuantityFieldMixin, self).__init__(*args, **kwargs)

    @property
    def units(self):
        return self.base_units

    def deconstruct(self):
        name, path, args, kwargs = super(QuantityFieldMixin, self).deconstruct()
        kwargs["base_units"] = self.base_units
        kwargs["unit_choices"] = self.unit_choices
        return name, path, args, kwargs

    def get_prep_value(self, value):
        # we store the value in the base units defined for this field
        if value is None:
            return None

        # Check if not the DeconstructibleUnitRegistry from this module but the default
        # UnitRegistery from pint was used
        if isinstance(value, Quantity) and not isinstance(value, self.ureg.Quantity):
            # Could be fatal if different unit registers are used but we assume
            # the same is used within one project
            # so we might need to implement a check if the UnitRegisters do match
            warnings.warn(
                "Trying to set value from a different unit register for quantityfield. "
                "We assume the naming is equal but best use the same register as for"
                " creating the quantityfield.",
                RuntimeWarning,
            )
            value = value.magnitude * self.ureg(str(value.units))

        if isinstance(value, self.ureg.Quantity):
            to_save = value.to(self.base_units)
            return self.to_number_type(to_save.magnitude)
        return value

    def value_to_string(self, obj) -> str:
        value = self.value_from_object(obj)
        return str(self.get_prep_value(value))

    def from_db_value(self, value, *args, **kwargs):
        if value is None:
            return value
        return self.ureg.Quantity(value * getattr(self.ureg, self.base_units))

    def to_python(self, value):
        if isinstance(value, self.ureg.Quantity):
            return value

        if value is None:
            return None

        return self.ureg.Quantity(value * getattr(self.ureg, self.base_units))

    # TODO: Add tests, understand, add super call if required
    """
    # This code is untested and not documented. It also does not call the super method
    Therefore it is commented out for the moment (even so it is likely required)

    def get_prep_lookup(self, lookup_type, value):

        if lookup_type in ["lt", "gt", "lte", "gte"]:
            if isinstance(value, self.ureg.Quantity):
                v = value.to(self.base_units)
                return v.magnitude
            return value
    """

    def formfield(self, **kwargs):
        defaults = {
            "form_class": self.form_field_class,
            "base_units": self.base_units,
            "unit_choices": self.unit_choices,
        }
        defaults.update(kwargs)
        return super(QuantityFieldMixin, self).formfield(**defaults)


class QuantityFormFieldMixin(object):
    """This formfield allows a user to choose which units they
    wish to use to enter a value, but the value is yielded in
    the base_units
    """

    to_number_type = NotImplemented

    def __init__(self, *args, **kwargs):
        self.ureg = ureg
        self.base_units = kwargs.pop("base_units", None)
        if self.base_units is None:
            raise ValueError(
                "QuantityFormField requires a base_units kwarg of a "
                "single unit type (eg: grams)"
            )
        self.units = kwargs.pop("unit_choices", [self.base_units])
        if self.base_units not in self.units:
            self.units.append(self.base_units)

        check_matching_unit_dimension(self.ureg, self.base_units, self.units)

        kwargs["widget"] = kwargs.get(
            "widget",
            QuantityWidget(base_units=self.base_units, allowed_types=self.units),
        )
        super(QuantityFormFieldMixin, self).__init__(*args, **kwargs)

    def prepare_value(self, value):

        if isinstance(value, Quantity):
            return value.to(self.base_units)
        else:
            return value

    def clean(self, value):
        """
        General idea, first try to extract the correct number like done in the other
        classes and then follow the same procedure as in the django default field
        """
        if isinstance(value, list) or isinstance(value, tuple):
            val = value[0]
            units = value[1]
        else:
            # If no multi widget is used
            val = value
            units = self.base_units

        if val in self.empty_values:
            # Make sure the correct functions are called also in case of empty values
            self.validate(None)
            self.run_validators(None)
            return None

        if units not in self.units:
            raise ValidationError("%(units)s is not a valid choice" % locals())

        if self.localize:
            val = formats.sanitize_separators(value)

        try:
            val = self.to_number_type(val)
        except PrecisionLoss as e:
            raise ValidationError(str(e), code="precision_loss")
        except (ValueError, TypeError):
            raise ValidationError(self.error_messages["invalid"], code="invalid")

        val = self.ureg.Quantity(val * getattr(self.ureg, units)).to(self.base_units)
        self.validate(val.magnitude)
        self.run_validators(val)
        return val


class QuantityFormField(QuantityFormFieldMixin, forms.FloatField):
    to_number_type = float


class QuantityField(QuantityFieldMixin, models.FloatField):
    form_field_class = QuantityFormField
    to_number_type = float


class IntegerQuantityFormField(QuantityFormFieldMixin, forms.IntegerField):
    to_number_type = staticmethod(safe_to_int)


class IntegerQuantityField(QuantityFieldMixin, models.IntegerField):
    form_field_class = IntegerQuantityFormField
    to_number_type = staticmethod(safe_to_int)


class BigIntegerQuantityField(QuantityFieldMixin, models.BigIntegerField):
    form_field_class = IntegerQuantityFormField
    to_number_type = staticmethod(safe_to_int)
