"""Entity validator — Logic Track (D-VAL-01~02)."""

import pytest


def test_d_val_01_reject_unsupported_unit_inch():
    """D-VAL-01: 미지원 단위 inch → 거부 (control에서 E002 매핑 예정)."""
    # Given: 미지원 단위 inch와 유효한 양수 값
    unit = "inch"
    value = 1.0

    # When / Then: validate(unit, value) — 지원 단위(meter, feet, yard) 외 거부
    from src.entity.validator import validate

    with pytest.raises(ValueError, match="Unsupported unit: inch"):
        validate(unit, value)


def test_d_val_02_reject_negative_value():
    """D-VAL-02: 음수 값 -1 → 거부 (control에서 E003 매핑 예정)."""
    # Given: 지원 단위 meter와 음수 값 -1
    unit = "meter"
    value = -1.0

    # When / Then: validate(unit, value) — 음수 입력 거부
    from src.entity.validator import validate

    with pytest.raises(ValueError, match="Value must not be negative"):
        validate(unit, value)
