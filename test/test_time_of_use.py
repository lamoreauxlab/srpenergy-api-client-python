"""The tests for the Srp Energy API Time of Use cases."""
from datetime import datetime
from test.common import MOCK_LOGIN_RESPONSE  # pylint: disable=R0801
from test.common import (
    PATCH_GET,
    PATCH_POST,
    TEST_PASSWORD,
    TEST_USER_NAME,
    get_mock_requests,
)
from unittest.mock import patch

from srpenergy.client import SrpEnergyClient

TEST_ACCOUNT_TOU_ID = "987654321"

MOCK_USAGE_TOU_SUMMER_OFF_PEAK_RESPONSE = {
    "hourlyUsageList": (
        {
            "date": "2020-06-24T00:00:00",
            "hour": "2020-06-24T00:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 6.1,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.00,
        },
        {
            "date": "2020-06-24T01:00:00",
            "hour": "2020-06-24T01:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 5.2,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.00,
        },
        {
            "date": "2020-06-24T02:00:00",
            "hour": "2020-06-24T02:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 5.3,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.00,
        },
    ),
    "demandList": (),
}

MOCK_USAGE_TOU_SUMMER_ON_PEAK_RESPONSE = {
    "hourlyUsageList": (
        {
            "date": "2020-06-25T17:00:00",
            "hour": "2020-06-25T17:00:00",
            "onPeakKwh": 6.5,
            "offPeakKwh": 0.0,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.00,
        },
        {
            "date": "2020-06-25T18:00:00",
            "hour": "2020-06-25T18:00:00",
            "onPeakKwh": 6.8,
            "offPeakKwh": 0.0,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.00,
        },
        {
            "date": "2020-06-25T19:00:00",
            "hour": "2020-06-25T19:00:00",
            "onPeakKwh": 3.7,
            "offPeakKwh": 0.0,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.00,
        },
    ),
    "demandList": (),
}

MOCK_USAGE_TOU_PEAK_SUMMER_OFF_PEAK_RESPONSE = {
    "hourlyUsageList": (
        {
            "date": "2019-07-24T00:00:00",
            "hour": "2019-07-24T00:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 7.1,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.00,
        },
        {
            "date": "2019-07-24T01:00:00",
            "hour": "2019-07-24T01:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 6.2,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.00,
        },
        {
            "date": "2019-07-24T02:00:00",
            "hour": "2019-07-24T02:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 6.3,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.00,
        },
    ),
    "demandList": (),
}

MOCK_USAGE_TOU_PEAK_SUMMER_ON_PEAK_RESPONSE = {
    "hourlyUsageList": (
        {
            "date": "2019-07-24T17:00:00",
            "hour": "2019-07-24T17:00:00",
            "onPeakKwh": 7.5,
            "offPeakKwh": 0.0,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.00,
        },
        {
            "date": "2019-07-24T18:00:00",
            "hour": "2019-07-24T18:00:00",
            "onPeakKwh": 7.8,
            "offPeakKwh": 0.0,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.00,
        },
        {
            "date": "2019-07-24T19:00:00",
            "hour": "2019-07-24T19:00:00",
            "onPeakKwh": 4.7,
            "offPeakKwh": 0.0,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.00,
        },
    ),
    "demandList": (),
}

MOCK_USAGE_TOU_WINTER_OFF_PEAK_RESPONSE = {
    "hourlyUsageList": (
        {
            "date": "2019-12-20T00:00:00",
            "hour": "2019-12-20T00:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 2.1,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.00,
        },
        {
            "date": "2019-12-20T01:00:00",
            "hour": "2019-12-20T01:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 1.2,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.00,
        },
        {
            "date": "2019-12-20T02:00:00",
            "hour": "2019-12-20T02:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 1.3,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.00,
        },
    ),
    "demandList": (),
}

MOCK_USAGE_TOU_WINTER_ON_PEAK_RESPONSE = {
    "hourlyUsageList": (
        {
            "date": "2019-12-19T17:00:00",
            "hour": "2019-12-19T17:00:00",
            "onPeakKwh": 2.5,
            "offPeakKwh": 0.0,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.00,
        },
        {
            "date": "2019-12-19T18:00:00",
            "hour": "2019-12-19T18:00:00",
            "onPeakKwh": 2.8,
            "offPeakKwh": 0.0,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.00,
        },
        {
            "date": "2019-12-19T19:00:00",
            "hour": "2019-12-19T19:00:00",
            "onPeakKwh": 0.7,
            "offPeakKwh": 0.0,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.00,
        },
    ),
    "demandList": (),
}

ROUTES = [
    ("06-24-2020", MOCK_USAGE_TOU_SUMMER_OFF_PEAK_RESPONSE),
    ("06-25-2020", MOCK_USAGE_TOU_SUMMER_ON_PEAK_RESPONSE),
    ("07-24-2019", MOCK_USAGE_TOU_PEAK_SUMMER_OFF_PEAK_RESPONSE),
    ("07-23-2019", MOCK_USAGE_TOU_PEAK_SUMMER_ON_PEAK_RESPONSE),
    ("12-20-2019", MOCK_USAGE_TOU_WINTER_OFF_PEAK_RESPONSE),
    ("12-19-2019", MOCK_USAGE_TOU_WINTER_ON_PEAK_RESPONSE),
]


def test_time_of_use_summer_off_peak_usage():
    """Test Time of Use for summer Off Peak Usage for kwh."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.side_effect = get_mock_requests(ROUTES)

        client = SrpEnergyClient(TEST_ACCOUNT_TOU_ID, TEST_USER_NAME, TEST_PASSWORD)

        start_date = datetime(2020, 6, 24, 0, 0, 0)
        end_date = datetime(2020, 6, 24, 23, 0, 0)

        usage = client.usage(start_date, end_date, True)

        assert len(usage) == 3

        _date, _hour, _isodate, kwh, cost = usage[0]

        assert kwh == 6.1
        assert cost == 0.44


def test_time_of_use_summer_on_peak_usage():
    """Test Time of Use for summer on Peak Usage for kwh."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.side_effect = get_mock_requests(ROUTES)

        client = SrpEnergyClient(TEST_ACCOUNT_TOU_ID, TEST_USER_NAME, TEST_PASSWORD)

        start_date = datetime(2020, 6, 25, 0, 0, 0)
        end_date = datetime(2020, 6, 25, 23, 0, 0)

        usage = client.usage(start_date, end_date, True)

        assert len(usage) == 3

        _date, _hour, _isodate, kwh, cost = usage[0]

        assert kwh == 6.5
        assert cost == 1.36


def test_time_of_use_peak_summer_off_peak_usage():
    """Test Time of Use for peak summer Off Peak Usage for kwh."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.side_effect = get_mock_requests(ROUTES)

        client = SrpEnergyClient(TEST_ACCOUNT_TOU_ID, TEST_USER_NAME, TEST_PASSWORD)

        start_date = datetime(2019, 7, 24, 0, 0, 0)
        end_date = datetime(2019, 7, 24, 23, 0, 0)

        usage = client.usage(start_date, end_date, True)

        assert len(usage) == 3

        _date, _hour, _isodate, kwh, cost = usage[0]

        assert kwh == 7.1
        assert cost == 0.52


def test_time_of_use_peak_summer_on_peak_usage():
    """Test Time of Use for peak summer on Peak Usage for kwh."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.side_effect = get_mock_requests(ROUTES)

        client = SrpEnergyClient(TEST_ACCOUNT_TOU_ID, TEST_USER_NAME, TEST_PASSWORD)

        start_date = datetime(2019, 7, 23, 0, 0, 0)
        end_date = datetime(2019, 7, 23, 23, 0, 0)

        usage = client.usage(start_date, end_date, True)

        assert len(usage) == 3

        _date, _hour, _isodate, kwh, cost = usage[0]

        assert kwh == 7.5
        assert cost == 1.81


def test_time_of_use_winter_off_peak_usage():
    """Test Time of Use for winter Off Peak Usage for kwh."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.side_effect = get_mock_requests(ROUTES)

        client = SrpEnergyClient(TEST_ACCOUNT_TOU_ID, TEST_USER_NAME, TEST_PASSWORD)

        start_date = datetime(2019, 12, 20, 0, 0, 0)
        end_date = datetime(2019, 12, 20, 23, 0, 0)

        usage = client.usage(start_date, end_date, True)

        assert len(usage) == 3

        _date, _hour, _isodate, kwh, cost = usage[0]

        assert kwh == 2.1
        assert cost == 0.15


def test_time_of_use_winter_on_peak_usage():
    """Test Time of Use for winter on Peak Usage for kwh."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.side_effect = get_mock_requests(ROUTES)

        client = SrpEnergyClient(TEST_ACCOUNT_TOU_ID, TEST_USER_NAME, TEST_PASSWORD)

        start_date = datetime(2019, 12, 19, 0, 0, 0)
        end_date = datetime(2019, 12, 19, 23, 0, 0)

        usage = client.usage(start_date, end_date, True)

        assert len(usage) == 3

        _date, _hour, _isodate, kwh, cost = usage[0]

        assert kwh == 2.5
        assert cost == 0.24
