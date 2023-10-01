from importlib.metadata import PackageNotFoundError, version

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "django-pint"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

from quantityfield import fields, helper, settings, units, widgets

__all__ = ["fields", "helper", "settings", "units", "widgets"]
