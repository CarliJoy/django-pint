import sys
import warnings

import django_pint


def test_version_import_django_pint() -> None:
    """The django_pint version is a defined version"""
    assert django_pint.__version__ != "unknown"
    assert django_pint.__version__[0].isnumeric()


def test_quantityfield_emits_deprecation_warning() -> None:
    """Importing the quantityfield package emits a DeprecationWarning"""
    # Remove cached module to force re-import and re-execution of __init__.py
    sys.modules.pop("quantityfield", None)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        import quantityfield  # noqa: F401

        deprecation_warnings = [
            w for w in caught if issubclass(w.category, DeprecationWarning)
        ]
        assert len(deprecation_warnings) >= 1
        assert "quantityfield" in str(deprecation_warnings[0].message).lower()
        assert "django_pint" in str(deprecation_warnings[0].message).lower()

    assert quantityfield.__version__ != "unknown"
    assert quantityfield.__version__[0].isnumeric()


def test_quantityfield_submodule_import_emits_deprecation_warning() -> None:
    """Importing a submodule of quantityfield also triggers a DeprecationWarning"""
    # Remove cached modules to force re-import
    for mod in list(sys.modules):
        if mod == "quantityfield" or mod.startswith("quantityfield."):
            sys.modules.pop(mod, None)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        from quantityfield import fields as _qf_fields  # noqa: F401

        deprecation_warnings = [
            w for w in caught if issubclass(w.category, DeprecationWarning)
        ]
        assert len(deprecation_warnings) >= 1
        assert "quantityfield" in str(deprecation_warnings[0].message).lower()
        assert "django_pint" in str(deprecation_warnings[0].message).lower()


def test_quantityfield_version_matches_django_pint() -> None:
    """quantityfield and django_pint report the same version"""
    import quantityfield

    assert quantityfield.__version__ == django_pint.__version__


def test_django_pint_fields_importable() -> None:
    """All field classes can be imported from django_pint.fields"""
    from django_pint.fields import (
        BigIntegerQuantityField,
        DecimalQuantityField,
        DecimalQuantityFormField,
        IntegerQuantityField,
        IntegerQuantityFormField,
        PositiveIntegerQuantityField,
        QuantityField,
        QuantityFieldMixin,
        QuantityFormField,
        QuantityFormFieldMixin,
    )

    assert QuantityField is not None
    assert QuantityFieldMixin is not None
    assert QuantityFormField is not None
    assert QuantityFormFieldMixin is not None
    assert IntegerQuantityField is not None
    assert IntegerQuantityFormField is not None
    assert BigIntegerQuantityField is not None
    assert PositiveIntegerQuantityField is not None
    assert DecimalQuantityField is not None
    assert DecimalQuantityFormField is not None


def test_quantityfield_fields_re_exports_from_django_pint() -> None:
    """quantityfield.fields re-exports all field and form-field classes from django_pint.fields"""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from quantityfield import fields as qf_fields

    from django_pint import fields as dp_fields

    assert qf_fields.QuantityField is dp_fields.QuantityField
    assert qf_fields.QuantityFieldMixin is dp_fields.QuantityFieldMixin
    assert qf_fields.QuantityFormField is dp_fields.QuantityFormField
    assert qf_fields.QuantityFormFieldMixin is dp_fields.QuantityFormFieldMixin
    assert qf_fields.IntegerQuantityField is dp_fields.IntegerQuantityField
    assert qf_fields.IntegerQuantityFormField is dp_fields.IntegerQuantityFormField
    assert qf_fields.BigIntegerQuantityField is dp_fields.BigIntegerQuantityField
    assert (
        qf_fields.PositiveIntegerQuantityField is dp_fields.PositiveIntegerQuantityField
    )
    assert qf_fields.DecimalQuantityField is dp_fields.DecimalQuantityField
    assert qf_fields.DecimalQuantityFormField is dp_fields.DecimalQuantityFormField


def test_django_pint_units_importable() -> None:
    """ureg can be imported from django_pint.units"""
    from django_pint.units import ureg

    assert ureg is not None


def test_quantityfield_units_re_exports_from_django_pint() -> None:
    """quantityfield.units re-exports ureg from django_pint.units"""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from quantityfield import units as qf_units

    from django_pint import units as dp_units

    assert qf_units.ureg is dp_units.ureg


def test_django_pint_widgets_importable() -> None:
    """QuantityWidget can be imported from django_pint.widgets"""
    from django_pint.widgets import QuantityWidget

    assert QuantityWidget is not None


def test_quantityfield_widgets_re_exports_from_django_pint() -> None:
    """quantityfield.widgets re-exports QuantityWidget from django_pint.widgets"""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from quantityfield import widgets as qf_widgets

    from django_pint import widgets as dp_widgets

    assert qf_widgets.QuantityWidget is dp_widgets.QuantityWidget


def test_django_pint_helper_importable() -> None:
    """check_matching_unit_dimension can be imported from django_pint.helper"""
    from django_pint.helper import check_matching_unit_dimension

    assert check_matching_unit_dimension is not None


def test_quantityfield_helper_re_exports_from_django_pint() -> None:
    """quantityfield.helper re-exports check_matching_unit_dimension from django_pint.helper"""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from quantityfield import helper as qf_helper

    from django_pint import helper as dp_helper

    assert (
        qf_helper.check_matching_unit_dimension
        is dp_helper.check_matching_unit_dimension
    )


def test_django_pint_settings_importable() -> None:
    """DJANGO_PINT_UNIT_REGISTER can be imported from django_pint.settings"""
    from django_pint.settings import DJANGO_PINT_UNIT_REGISTER

    assert DJANGO_PINT_UNIT_REGISTER is not None


def test_quantityfield_settings_re_exports_from_django_pint() -> None:
    """quantityfield.settings re-exports DJANGO_PINT_UNIT_REGISTER from django_pint.settings"""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from quantityfield import settings as qf_settings

    from django_pint import settings as dp_settings

    assert (
        qf_settings.DJANGO_PINT_UNIT_REGISTER is dp_settings.DJANGO_PINT_UNIT_REGISTER
    )
