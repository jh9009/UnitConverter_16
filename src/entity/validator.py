"""Domain validation for length unit conversion inputs."""

SUPPORTED_UNITS = frozenset({"meter", "feet", "yard"})


def validate(unit: str, value: float) -> None:
    """Raise ValueError for unsupported units or negative values."""
    if unit not in SUPPORTED_UNITS:
        raise ValueError(f"Unsupported unit: {unit}")
    if value < 0:
        raise ValueError("Value must not be negative")
