from pkg_resources import DistributionNotFound, get_distribution

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "django-pint"
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:  # pragma: no cover
    # We don't expect this to be executed, as this would mean the configuration
    # for the python module is wrong
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound
