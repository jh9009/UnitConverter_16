"""Entity converter — Logic Track (D-CNV-01~03)."""

import pytest


def test_d_cnv_01_to_meter_one_feet():
    """D-CNV-01: 1 feet → 0.3048 m (±ε, SSOT)."""
    # Given: 1 feet 입력값, SSOT 기대값 0.3048 m (±ε)
    value = 1.0
    unit = "feet"

    # When: to_meter(value, unit) — SSOT 상수에서 비율 로드 후 미터 환산
    from src.entity.converter import to_meter

    result = to_meter(value, unit)

    # Then:
    assert result == pytest.approx(0.3048, rel=1e-5)


def test_d_cnv_02_convert_all_meter_to_feet():
    """D-CNV-02: 2.5 m → 8.20210 ft (소수 5자리)."""
    # Given: 2.5 meter 입력값, 기대 feet 출력 8.20210 (5 decimals)
    value = 2.5
    unit = "meter"

    # When: convert_all(value, unit) — meter·feet·yard 일괄 변환
    from src.entity.converter import convert_all

    result = convert_all(value, unit)

    # Then:
    assert result["feet"] == pytest.approx(8.20210, rel=1e-5)


def test_d_cnv_03_convert_all_feet_to_yard_via_meter():
    """D-CNV-03: feet → yard, meter 경유 일관성."""
    # Given: feet 입력값, meter 경유 feet·yard 변환 결과가 SSOT 비율과 일치
    value = 3.0
    unit = "feet"

    # When: convert_all(value, unit) — feet→meter→yard 경로로 yard 산출
    from src.entity.constants import METERS_PER_FOOT, METERS_PER_YARD
    from src.entity.converter import convert_all

    result = convert_all(value, unit)
    meters = value * METERS_PER_FOOT
    expected_yard = meters / METERS_PER_YARD

    # Then:
    assert result["meter"] == pytest.approx(meters, rel=1e-5)
    assert result["feet"] == pytest.approx(value, rel=1e-5)
    assert result["yard"] == pytest.approx(expected_yard, rel=1e-5)
