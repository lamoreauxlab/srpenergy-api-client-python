"""The tests for the Srp Energy API Rate calculation."""

import pytest

from srpenergy.client import get_rate


def test_winter_off_peak():
    """Test Winter off peak price."""
    usage_time = "2020-01-24T01:00:00"
    rate, is_on_peak = get_rate(usage_time)

    assert rate == 0.0691
    assert is_on_peak is False


def test_winter_on_peak():
    """Test Winter on peak price."""
    usage_time = "2020-01-24T05:00:00"
    rate, is_on_peak = get_rate(usage_time)

    assert rate == 0.0951
    assert is_on_peak is True


def test_summer_off_peak():
    """Test summer off peak price."""
    usage_time = "2020-06-24T01:00:00"
    rate, is_on_peak = get_rate(usage_time)

    assert rate == 0.0727
    assert is_on_peak is False


def test_summer_on_peak():
    """Test Summer on peak price."""
    usage_time = "2020-06-24T15:00:00"
    rate, is_on_peak = get_rate(usage_time)

    assert rate == 0.2094
    assert is_on_peak is True


def test_peak_summer_off_peak():
    """Test peak summer off peak price."""
    usage_time = "2020-07-24T01:00:00"
    rate, is_on_peak = get_rate(usage_time)

    assert rate == 0.073
    assert is_on_peak is False


def test_peak_summer_on_peak():
    """Test peak summer on peak price."""
    usage_time = "2020-07-24T15:00:00"
    rate, is_on_peak = get_rate(usage_time)

    assert rate == 0.2409
    assert is_on_peak is True


def test_winter_weekend():
    """Test Winter weekend price."""
    usage_time = "2020-02-08T6:00:00"
    rate, is_on_peak = get_rate(usage_time)

    assert rate == 0.0691
    assert is_on_peak is False


def test_summer_weekend():
    """Test summer weekend price."""
    usage_time = "2020-06-27T15:00:00"
    rate, is_on_peak = get_rate(usage_time)

    assert rate == 0.0727
    assert is_on_peak is False


def test_peak_summer_weekend():
    """Test peak summer weekend price."""
    usage_time = "2020-07-18T15:00:00"
    rate, is_on_peak = get_rate(usage_time)

    assert rate == 0.073
    assert is_on_peak is False


def test_winter_new_years():
    """Test Winter new years price."""
    usage_time = "2020-01-01T06:00:00"
    rate, is_on_peak = get_rate(usage_time)

    assert rate == 0.0691
    assert is_on_peak is False


def test_summer_memorial_day():
    """Test summer memorial day price."""
    usage_time = "2021-05-31T16:00:00"
    rate, is_on_peak = get_rate(usage_time)

    assert rate == 0.0727
    assert is_on_peak is False


def test_peak_summer_independence_day():
    """Test summer independence day price."""
    usage_time = "2019-07-04T16:00:00"
    rate, is_on_peak = get_rate(usage_time)

    assert rate == 0.073
    assert is_on_peak is False


def test_summer_labor_day():
    """Test summer labor day price."""
    usage_time = "2020-09-07T16:00:00"
    rate, is_on_peak = get_rate(usage_time)

    assert rate == 0.0727
    assert is_on_peak is False


def test_winter_thanksgiving_day():
    """Test winter thanksgiving day price."""
    usage_time = "2020-11-26T17:00:00"
    rate, is_on_peak = get_rate(usage_time)

    assert rate == 0.0691
    assert is_on_peak is False


def test_winter_christmas_day():
    """Test winter christmas day price."""
    usage_time = "2020-12-24T17:00:00"
    rate, is_on_peak = get_rate(usage_time)

    assert rate == 0.0691
    assert is_on_peak is False


def test_none_parameter():
    """Test none parameter."""
    with pytest.raises(TypeError):
        get_rate(None)


def test_bad_parameter():
    """Test parameter."""
    usage_time = "badvalue"

    with pytest.raises(ValueError):
        get_rate(usage_time)
