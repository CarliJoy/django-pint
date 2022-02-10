from pint import DimensionalityError


def check_matching_unit_dimension(ureg, base_units, units_to_check):
    """
    Check if all units_to_check have the same Dimension like the base_units
    If not
    :raise DimensionalityError
    """

    base_unit = getattr(ureg, base_units)

    for unit_string in units_to_check:
        unit = getattr(ureg, unit_string)
        if unit.dimensionality != base_unit.dimensionality:
            raise DimensionalityError(base_unit, unit)
