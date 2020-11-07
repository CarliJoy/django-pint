__version__ = "0.4"

from pint import UnitRegistry
from django.utils.deconstruct import deconstructible


@deconstructible
class DeconstructibleUnitRegistry(UnitRegistry):
    """Make UnitRegistry compatible with Django migrations by implementing the
    deconstruct() method."""


ureg = DeconstructibleUnitRegistry()
