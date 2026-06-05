"""Pure length unit conversion (meter, feet, yard)."""

from .constants import (
    FEET_PER_METER,
    METERS_PER_FOOT,
    METERS_PER_YARD,
    YARDS_PER_METER,
)

_TO_METER_FACTORS = {
    "meter": 1.0,
    "feet": METERS_PER_FOOT,
    "yard": METERS_PER_YARD,
}


def to_meter(value: float, unit: str) -> float:
    """Convert value in the given unit to meters."""
    factor = _TO_METER_FACTORS[unit]
    return value * factor


def convert_all(value: float, unit: str) -> dict[str, float]:
    """Convert value to all supported length units via meter."""
    meters = to_meter(value, unit)
    return {
        "meter": meters,
        "feet": meters * FEET_PER_METER,
        "yard": meters * YARDS_PER_METER,
    }
