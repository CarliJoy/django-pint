import warnings
from importlib.metadata import PackageNotFoundError, version

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "django-pint"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

warnings.warn(
    "The 'quantityfield' package is deprecated and will be removed in a future "
    "release. Please update your imports to use 'django_pint' instead.",
    DeprecationWarning,
    stacklevel=2,
)
