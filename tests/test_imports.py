import django_pint
import quantityfield


def test_version_import_quantityfield() -> None:
    """The quantityfield version is a defined version"""
    assert quantityfield.__version__ != "unknown"
    assert quantityfield.__version__[0].isnumeric()


def test_version_import_django_pint() -> None:
    """The django_pint version is a defined version"""
    assert django_pint.__version__ != "unknown"
    assert django_pint.__version__[0].isnumeric()
