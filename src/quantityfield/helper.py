from pint import DimensionalityError, UnitRegistry
from typing import List


def check_matching_unit_dimension(
    ureg: UnitRegistry, base_units: str, units_to_check: List[str]
) -> None:
    """
    Check if all units_to_check have the same Dimension like the base_units
    If not
    :raise DimensionalityError
    """
    base_unit = getattr(ureg, base_units)
    # create a pint quantity by multiplying unit with magnitude of 1
    base_quant = 1 * base_unit

    for unit_string in units_to_check:
        unit = getattr(ureg, unit_string)
        # try to convert base qunatity to new unit, this also work for ureg.context
        try:
            base_quant.to(unit)
        except DimensionalityError as e:
            raise DimensionalityError(base_unit, unit) from e
