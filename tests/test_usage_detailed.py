"""The tests for SrpEnergyClient.usage_detailed()."""

from datetime import datetime
from unittest.mock import Mock, patch

from srpenergy.client import SrpEnergyClient

from tests.common import (
    MOCK_LOGIN_RESPONSE,
    PATCH_GET,
    PATCH_POST,
    TEST_PASSWORD,
    TEST_USER_NAME,
    get_mock_requests,
)

TEST_ACCOUNT_ID = "123456789"

# A single TOU (EZ-3) hour with all four buckets populated with distinctive,
# non-zero values, so the test proves each bucket is passed through
# correctly and not accidentally collapsed, swapped, or dropped.
MOCK_USAGE_DETAILED_RESPONSE = {
    "hourlyUsageList": (
        {
            "date": "2026-09-04T15:00:00",
            "hour": "2026-09-04T15:00:00",
            "onPeakKwh": 8.4,
            "offPeakKwh": 0.0,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 2.03,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2026-09-04T00:00:00",
            "hour": "2026-09-04T00:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 1.7,
            "shoulderKwh": 0.3,
            "superOffPeakKwh": 0.1,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.16,
            "shoulderCost": 0.05,
            "superOffPeakCost": 0.01,
            "totalCost": 0.0,
        },
    ),
    "demandList": (),
}

# A non-TOU (standard rate) hour: SRP populates totalKwh/totalCost directly
# and all four tariff buckets are 0.
MOCK_USAGE_DETAILED_STANDARD_RATE_RESPONSE = {
    "hourlyUsageList": (
        {
            "date": "2019-10-09T00:00:00",
            "hour": "2019-10-09T00:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 0.0,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.4,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.08,
        },
    ),
    "demandList": (),
}

ROUTES_DETAILED = [("usage/hourlydetail", MOCK_USAGE_DETAILED_RESPONSE)]
ROUTES_DETAILED_STANDARD = [
    ("usage/hourlydetail", MOCK_USAGE_DETAILED_STANDARD_RATE_RESPONSE)
]


def test_usage_detailed_returns_all_buckets_for_tou_account() -> None:
    """Test usage_detailed preserves the full per-tariff-bucket breakdown."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:
        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.side_effect = get_mock_requests(ROUTES_DETAILED)

        client = SrpEnergyClient(TEST_ACCOUNT_ID, TEST_USER_NAME, TEST_PASSWORD)

        start_date = datetime(2026, 9, 4, 0, 0, 0)
        end_date = datetime(2026, 9, 4, 23, 0, 0)

        result = client.usage_detailed(start_date, end_date)

        assert len(result) == 2

        on_peak_hour = result[0]
        assert on_peak_hour["on_peak_kwh"] == 8.4
        assert on_peak_hour["on_peak_cost"] == 2.03
        assert on_peak_hour["off_peak_kwh"] == 0.0
        assert on_peak_hour["total_kwh"] == 8.4
        assert on_peak_hour["total_cost"] == 2.03

        mixed_hour = result[1]
        assert mixed_hour["off_peak_kwh"] == 1.7
        assert mixed_hour["off_peak_cost"] == 0.16
        assert mixed_hour["shoulder_kwh"] == 0.3
        assert mixed_hour["shoulder_cost"] == 0.05
        assert mixed_hour["super_off_peak_kwh"] == 0.1
        assert mixed_hour["super_off_peak_cost"] == 0.01
        # total should be the sum of all four buckets, not just one
        assert round(mixed_hour["total_kwh"], 2) == 2.1
        assert round(mixed_hour["total_cost"], 2) == 0.22


def test_usage_detailed_standard_rate_account_uses_total_fields() -> None:
    """Test usage_detailed for a non-TOU account returns 0 buckets and a real total."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:
        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.side_effect = get_mock_requests(ROUTES_DETAILED_STANDARD)

        client = SrpEnergyClient(TEST_ACCOUNT_ID, TEST_USER_NAME, TEST_PASSWORD)

        start_date = datetime(2019, 10, 9, 0, 0, 0)
        end_date = datetime(2019, 10, 9, 23, 0, 0)

        result = client.usage_detailed(start_date, end_date)

        assert len(result) == 1
        row = result[0]
        assert row["on_peak_kwh"] == 0.0
        assert row["off_peak_kwh"] == 0.0
        assert row["shoulder_kwh"] == 0.0
        assert row["super_off_peak_kwh"] == 0.0
        assert row["total_kwh"] == 0.4
        assert row["total_cost"] == 0.08


def test_usage_detailed_bad_start_date_raises_value_error() -> None:
    """Test usage_detailed validates startdate like usage() does."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:
        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.side_effect = get_mock_requests(ROUTES_DETAILED)

        client = SrpEnergyClient(TEST_ACCOUNT_ID, TEST_USER_NAME, TEST_PASSWORD)
        end_date = datetime(2026, 9, 4, 23, 0, 0)

        try:
            client.usage_detailed("20260904", end_date)
            raise AssertionError("Expected ValueError")
        except ValueError:
            pass
