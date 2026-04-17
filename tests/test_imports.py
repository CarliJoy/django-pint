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
    """quantityfield.fields re-exports all classes from django_pint.fields"""
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from quantityfield import fields as qf_fields

    from django_pint import fields as dp_fields

    assert qf_fields.QuantityField is dp_fields.QuantityField
    assert qf_fields.IntegerQuantityField is dp_fields.IntegerQuantityField
    assert qf_fields.BigIntegerQuantityField is dp_fields.BigIntegerQuantityField
    assert qf_fields.DecimalQuantityField is dp_fields.DecimalQuantityField


def test_django_pint_units_importable() -> None:
    """ureg can be imported from django_pint.units"""
    from django_pint.units import ureg

    assert ureg is not None


def test_django_pint_widgets_importable() -> None:
    """QuantityWidget can be imported from django_pint.widgets"""
    from django_pint.widgets import QuantityWidget

    assert QuantityWidget is not None


def test_django_pint_helper_importable() -> None:
    """check_matching_unit_dimension can be imported from django_pint.helper"""
    from django_pint.helper import check_matching_unit_dimension

    assert check_matching_unit_dimension is not None
