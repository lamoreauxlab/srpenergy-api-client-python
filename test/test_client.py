"""The tests for the Srp Energy API."""
from unittest.mock import patch
from datetime import datetime, timedelta
import collections
import pytest
from srpenergy.client import SrpEnergyClient

PATCH_GET = 'srpenergy.client.requests.Session.get'
PATCH_POST = 'srpenergy.client.requests.Session.post'
TEST_ACCOUNT_ID = '12345678'
TEST_USER_NAME = 'abba'
TEST_PASSWORD = 'dabba'

MockContent = collections.namedtuple('MockContent', 'content status_code')

MOCK_LOGIN_RESPONSE = MockContent(
    status_code=200,
    content=b'<!DOCTYPE html>\
    <html lang="en"><head><title>Sample</title></head>\
    <body><select name="accountNumber" id="AccountSelection">\
    <optgroup id="ElectricAccountSelect" label="My power accounts">\
    <option value="12345678" selected=&quot;selected&quot;>\
    123-456-789</option>\
    </optgroup><option value="newAccount">Add new account</option>\
    </select></body></html>')

MOCK_USAGE_RESPONSE = MockContent(
    status_code=200,
    content=b'Usage Date,Hour,kWh,Cost\r\n9/19/2018,\
12:00 AM,1.2,$0.17\r\n9/19/2018,1:00 AM,2.1,$0.30\r\ntotal'
)

MOCK_TIME_OF_USE_USAGE_RESPONSE = MockContent(
    status_code=200,
    content=b'Usage Date,Hour,kWh,Cost\r\n9/19/2018,\
12:00 AM,1.2,$0.17,off-peak\r\n9/19/2018,1:00 AM,2.1,$0.30,off-peak\r\ntotal')


# class MockLoginResponse:
#     """Represents a Mock Login Response for testing."""

#     def __init__(self, status_code):
#         """Define content for Mock Login."""
#         self.status_code = status_code
#         self.content = b'<!DOCTYPE html>\
#         <html lang="en"><head><title>Sample</title></head>\
#         <body><select name="accountNumber" id="AccountSelection">\
#         <optgroup id="ElectricAccountSelect" label="My power accounts">\
#         <option value="12345678" selected=&quot;selected&quot;>\
#         123-456-789</option>\
#         </optgroup><option value="newAccount">Add new account</option>\
#         </select></body></html>'


# class MockUsageResponse:
#     """Represents a Mock Usage Response for testing."""

#     def __init__(self, status_code):
#         """Define content for Mock Usage."""
#         self.status_code = status_code
#         self.content = b'Usage Date,Hour,kWh,Cost\r\n9/19/2018,\
# 12:00 AM,1.2,$0.17\r\n9/19/2018,1:00 AM,2.1,$0.30\r\ntotal'


# class MockTimeOfUseUsageResponse:
#     """Represents a Mock Usage Response for testing."""

#     def __init__(self, status_code):
#         """Define content for Mock Usage."""
#         self.status_code = status_code
#         self.content = b'Usage Date,Hour,kWh,Cost\r\n9/19/2018,\
# 12:00 AM,1.2,$0.17,off-peak\r\n9/19/2018,1:00 AM,2.1,$0.30,off-peak\r\ntotal'


def test_none_accountid():
    """Test No account parameter exception."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.return_value = MOCK_USAGE_RESPONSE

        with pytest.raises(TypeError):
            SrpEnergyClient(None, 'b', 'c')


def test_none_username():
    """Test No username parameter exception."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.return_value = MOCK_USAGE_RESPONSE

        with pytest.raises(TypeError):
            SrpEnergyClient('a', None, 'c')


def test_none_password():
    """Test No password parameter exception."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.return_value = MOCK_USAGE_RESPONSE

        with pytest.raises(TypeError):
            SrpEnergyClient('a', 'b', None)


def test_blank_accountid():
    """Test blank account parameter exception."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.return_value = MOCK_USAGE_RESPONSE

        with pytest.raises(ValueError):
            SrpEnergyClient('', 'b', 'c')


def test_blank_username():
    """Test blank username parameter exception."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.return_value = MOCK_USAGE_RESPONSE

        with pytest.raises(ValueError):
            SrpEnergyClient('a', '', 'c')


def test_blank_password():
    """Test blank password parameter exception."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.return_value = MOCK_USAGE_RESPONSE

        with pytest.raises(ValueError):
            SrpEnergyClient('a', 'b', '')


def test_bad_parameter_start_date_string():
    """Test start date is date."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.return_value = MOCK_USAGE_RESPONSE

        client = SrpEnergyClient(
            TEST_ACCOUNT_ID, TEST_USER_NAME,
            TEST_PASSWORD)

        end_date = datetime(2018, 10, 5, 12, 0, 0)

        with pytest.raises(ValueError):
            client.usage('20181001', end_date)


def test_bad_parameter_end_date_string():
    """Test end date is date."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.return_value = MOCK_USAGE_RESPONSE

        client = SrpEnergyClient(
            TEST_ACCOUNT_ID, TEST_USER_NAME,
            TEST_PASSWORD)

        start_date = datetime(2018, 10, 5, 12, 0, 0)

        with pytest.raises(ValueError):
            client.usage(start_date, '20181001')


def test_bad_parameter_start_date_after_now():
    """Test start date is not after Now."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.return_value = MOCK_USAGE_RESPONSE

        client = SrpEnergyClient(
            TEST_ACCOUNT_ID, TEST_USER_NAME, TEST_PASSWORD)

        start_date = datetime.now() + timedelta(days=10)
        end_date = datetime(2018, 10, 5, 12, 0, 0)

        with pytest.raises(ValueError):
            client.usage(start_date, end_date)


def test_bad_parameter_start_date_after_end_date():
    """Test start date is not after end date."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.return_value = MOCK_USAGE_RESPONSE

        client = SrpEnergyClient(
            TEST_ACCOUNT_ID, TEST_USER_NAME, TEST_PASSWORD)

        start_date = datetime(2018, 10, 6, 12, 0, 0)
        end_date = datetime(2018, 10, 5, 12, 0, 0)

        with pytest.raises(ValueError):
            client.usage(start_date, end_date)


def test_get_usage():
    """Test usage."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.return_value = MOCK_USAGE_RESPONSE

        client = SrpEnergyClient(
            TEST_ACCOUNT_ID, TEST_USER_NAME, TEST_PASSWORD)

        start_date = datetime(2018, 10, 1, 6, 0, 0)
        end_date = datetime(2018, 10, 5, 12, 0, 0)

        usage = client.usage(start_date, end_date)

        assert len(usage) == 2


def test_single_day_usage_kw():
    """Test Single Day Usage for kwh."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.return_value = MOCK_USAGE_RESPONSE

        client = SrpEnergyClient(
            TEST_ACCOUNT_ID, TEST_USER_NAME, TEST_PASSWORD)

        start_date = datetime(2018, 9, 19, 0, 0, 0)
        end_date = datetime(2018, 9, 19, 23, 0, 0)

        usage = client.usage(start_date, end_date)

        assert len(usage) == 2

        _date, _hour, _isodate, kwh, cost = usage[0]

        assert kwh == '1.2'
        assert cost == '0.17'


def test_latest_day_usage_kw():
    """Test Latest Day Usage for kwh."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.return_value = MOCK_USAGE_RESPONSE

        client = SrpEnergyClient(
            TEST_ACCOUNT_ID, TEST_USER_NAME, TEST_PASSWORD)

        start_date = datetime(2018, 9, 19, 0, 0, 0)
        end_date = datetime(2018, 9, 19, 23, 0, 0)

        usage = client.usage(start_date, end_date)

        assert len(usage) == 2

        _date, _hour, _isodate, kwh, cost = usage[-1]

        assert kwh == '2.1'
        assert cost == '0.30'


def test_time_of_use():
    """Test Time of use in usage."""
    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:

        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.return_value = MOCK_TIME_OF_USE_USAGE_RESPONSE

        client = SrpEnergyClient(
            TEST_ACCOUNT_ID, TEST_USER_NAME, TEST_PASSWORD)

        start_date = datetime(2018, 9, 19, 0, 0, 0)
        end_date = datetime(2018, 9, 19, 23, 0, 0)
        usage = client.usage(start_date, end_date)

        assert len(usage) == 2

        _date, _hour, _isodate, kwh, _cost = usage[-1]
        assert kwh == '2.1'
