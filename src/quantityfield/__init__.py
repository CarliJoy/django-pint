__version__ = "0.4"

from django.utils.deconstruct import deconstructible

from pint import UnitRegistry


@deconstructible
class DeconstructibleUnitRegistry(UnitRegistry):
    """Make UnitRegistry compatible with Django migrations by implementing the
    deconstruct() method."""


ureg = DeconstructibleUnitRegistry()
