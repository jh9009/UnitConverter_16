"""Pure length unit conversion (meter, feet, yard)."""

from .constants import (
    FEET_PER_METER,
    METERS_PER_FOOT,
    METERS_PER_YARD,
    UNIT_FEET,
    UNIT_METER,
    UNIT_YARD,
    YARDS_PER_METER,
)

_TO_METER_FACTORS = {
    UNIT_METER: 1.0,
    UNIT_FEET: METERS_PER_FOOT,
    UNIT_YARD: METERS_PER_YARD,
}


def to_meter(value: float, unit: str) -> float:
    """Convert value in the given unit to meters."""
    try:
        factor = _TO_METER_FACTORS[unit]
    except KeyError:
        raise ValueError(f"Unsupported unit: {unit}") from None
    return value * factor


def convert_all(value: float, unit: str) -> dict[str, float]:
    """Convert value to all supported length units via meter."""
    meters = to_meter(value, unit)
    return {
        UNIT_METER: meters,
        UNIT_FEET: meters * FEET_PER_METER,
        UNIT_YARD: meters * YARDS_PER_METER,
    }
