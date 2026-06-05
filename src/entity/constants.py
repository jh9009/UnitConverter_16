"""SSOT length conversion ratios and unit identifiers (meter as base unit)."""

UNIT_METER = "meter"
UNIT_FEET = "feet"
UNIT_YARD = "yard"

ALL_UNITS = (UNIT_METER, UNIT_FEET, UNIT_YARD)

FEET_PER_METER = 3.28084
YARDS_PER_METER = 1.09361

METERS_PER_FOOT = 1 / FEET_PER_METER
METERS_PER_YARD = 1 / YARDS_PER_METER
