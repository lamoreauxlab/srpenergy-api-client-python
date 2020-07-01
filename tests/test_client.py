"""The tests for the Srp Energy API."""
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import pytest

from srpenergy.client import SrpEnergyClient

from tests.common import (
    PATCH_GET,
    PATCH_POST,
    TEST_PASSWORD,
    TEST_USER_NAME,
    get_mock_requests,
)
from tests.common import MOCK_LOGIN_RESPONSE  # pylint: disable=R0801

TEST_ACCOUNT_ID = "123456789"
TEST_BAD_ACCOUNT_ID = "888999000"
MOCK_BAD_LOGIN_RESPONSE = Mock()
MOCK_BAD_LOGIN_RESPONSE.json.return_value = {
    "unpredected": "response",
}

MOCK_BAD_USAGE_RESPONSE = {
    "unpredected": "response",
}
MOCK_USAGE_RESPONSE = {
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
        {
            "date": "2019-10-09T01:00:00",
            "hour": "2019-10-09T01:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 0.0,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.5,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.09,
        },
        {
            "date": "2019-10-09T02:00:00",
            "hour": "2019-10-09T02:00:00",
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

ROUTES = [
    (TEST_BAD_ACCOUNT_ID, MOCK_BAD_USAGE_RESPONSE),
    ("usage/hourlydetail", MOCK_USAGE_RESPONSE),
]


def test_none_accountid():
    """Test No account parameter exception."""
    with pytest.raises(TypeError):
        SrpEnergyClient(None, "b", "c")


def test_none_username():
    """Test No username parameter exception."""
    with pytest.raises(TypeError):
        SrpEnergyClient(TEST_ACCOUNT_ID, None, "c")


def test_none_password():
    """Test No password parameter exception."""
    with pytest.raises(TypeError):
        SrpEnergyClient(TEST_ACCOUNT_ID, "b", None)


def test_blank_accountid():
    """Test blank account parameter exception."""
    with pytest.raises(ValueError):
        SrpEnergyClient("", "b", "c")


def test_blank_username():
    """Test blank username parameter exception."""
    with pytest.raises(ValueError):
        SrpEnergyClient(TEST_ACCOUNT_ID, "", "c")


def test_blank_password():
    """Test blank password parameter exception."""
    with pytest.raises(ValueError):
        SrpEnergyClient(TEST_ACCOUNT_ID, "b", "")


def test_bad_parameter_account_id_hyphens():
    """Test accountid has hybhens in it."""
    with pytest.raises(ValueError) as err_info:
        SrpEnergyClient("123-456", "b", "a")

    assert "Parameter account should only contain numbers." in str(err_info.value)


def test_bad_parameter_start_date_string():
    """Test start date is date."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.side_effect = get_mock_requests(ROUTES)

        client = SrpEnergyClient(TEST_ACCOUNT_ID, TEST_USER_NAME, TEST_PASSWORD)

        end_date = datetime(2018, 10, 5, 12, 0, 0)

        with pytest.raises(ValueError):
            client.usage("20181001", end_date)


def test_bad_parameter_end_date_string():
    """Test end date is date."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.side_effect = get_mock_requests(ROUTES)

        client = SrpEnergyClient(TEST_ACCOUNT_ID, TEST_USER_NAME, TEST_PASSWORD)

        start_date = datetime(2018, 10, 5, 12, 0, 0)

        with pytest.raises(ValueError):
            client.usage(start_date, "20181001")


def test_bad_parameter_start_date_after_now():
    """Test start date is not after Now."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.side_effect = get_mock_requests(ROUTES)

        client = SrpEnergyClient(TEST_ACCOUNT_ID, TEST_USER_NAME, TEST_PASSWORD)

        start_date = datetime.now() + timedelta(days=10)
        end_date = datetime.now() + timedelta(days=15)

        with pytest.raises(ValueError):
            client.usage(start_date, end_date)


def test_bad_parameter_start_date_after_end_date():
    """Test start date is not after end date."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.side_effect = get_mock_requests(ROUTES)

        client = SrpEnergyClient(TEST_ACCOUNT_ID, TEST_USER_NAME, TEST_PASSWORD)

        start_date = datetime(2018, 10, 6, 12, 0, 0)
        end_date = datetime(2018, 10, 5, 12, 0, 0)

        with pytest.raises(ValueError):
            client.usage(start_date, end_date)


def test_get_usage():
    """Test usage."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.side_effect = get_mock_requests(ROUTES)

        client = SrpEnergyClient(TEST_ACCOUNT_ID, TEST_USER_NAME, TEST_PASSWORD)

        start_date = datetime(2018, 10, 1, 6, 0, 0)
        end_date = datetime(2018, 10, 5, 12, 0, 0)

        usage = client.usage(start_date, end_date)

        assert len(usage) == 3


def test_single_day_usage_kw():
    """Test Single Day Usage for kwh."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.side_effect = get_mock_requests(ROUTES)

        client = SrpEnergyClient(TEST_ACCOUNT_ID, TEST_USER_NAME, TEST_PASSWORD)

        start_date = datetime(2018, 9, 19, 0, 0, 0)
        end_date = datetime(2018, 9, 19, 23, 0, 0)

        usage = client.usage(start_date, end_date)

        assert len(usage) == 3

        _date, _hour, _isodate, kwh, cost = usage[0]

        assert kwh == 0.4
        assert cost == 0.08


def test_latest_day_usage_kw():
    """Test Latest Day Usage for kwh."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.side_effect = get_mock_requests(ROUTES)

        client = SrpEnergyClient(TEST_ACCOUNT_ID, TEST_USER_NAME, TEST_PASSWORD)

        start_date = datetime(2018, 9, 19, 0, 0, 0)
        end_date = datetime(2018, 9, 19, 23, 0, 0)

        usage = client.usage(start_date, end_date)

        assert len(usage) == 3

        _date, _hour, _isodate, kwh, cost = usage[-1]

        assert kwh == 0.4
        assert cost == 0.08


def test_validate_user():
    """Test Validation of user."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.side_effect = get_mock_requests(ROUTES)

        client = SrpEnergyClient(TEST_ACCOUNT_ID, TEST_USER_NAME, TEST_PASSWORD)

        is_valid = client.validate()

        assert is_valid


def test_error_validate_user():
    """Test error Validation of user."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_BAD_LOGIN_RESPONSE
        session_get.side_effect = get_mock_requests(ROUTES)

        client = SrpEnergyClient(TEST_ACCOUNT_ID, TEST_USER_NAME, TEST_PASSWORD)

        is_valid = client.validate()

        assert is_valid is False


def test_error_usage_payload():
    """Test error with invalid usage payload."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.side_effect = get_mock_requests(ROUTES)

        client = SrpEnergyClient(TEST_BAD_ACCOUNT_ID, TEST_USER_NAME, TEST_PASSWORD)

        start_date = datetime(2018, 9, 19, 0, 0, 0)
        end_date = datetime(2018, 9, 19, 23, 0, 0)

        with pytest.raises(Exception):
            client.usage(start_date, end_date)
