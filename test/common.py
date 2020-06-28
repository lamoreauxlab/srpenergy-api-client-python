"""Shared methods and const for tests."""
from unittest.mock import Mock

PATCH_GET = "srpenergy.client.requests.Session.get"
PATCH_POST = "srpenergy.client.requests.Session.post"

TEST_USER_NAME = "abba"
TEST_PASSWORD = "dabba"

MOCK_LOGIN_RESPONSE = Mock()
MOCK_LOGIN_RESPONSE.json.return_value = {
    "message": "Log in successful.",
    "username": "user@example.com",
    "email": "user@example.com",
    "isIrrigator": False,
    "redirectUrl": "",
}

MOCK_ANTI_FORGERY_RESPONSE = {
    "message": "Success",
    "xsrfToken": "CfDJ8KUcoIlbMHV_NbT4uDyb-XA2|207f",
}


# pylint: disable=R0903
class MockResponse:
    """Mock Response."""

    def __init__(self, json_data, status_code, kwargs):
        """Create Mock Repsonse."""
        self.json_data = json_data
        self.status_code = status_code
        self.kwargs = kwargs

    def json(self):
        """Return mock json."""
        return self.json_data


def get_mock_requests(routes):
    """Return a function that can be mocked for the given routes."""
    # noqa: D202
    def mocked_requests_get(*args, **kwargs):

        if "login/antiforgerytoken" in args[0]:
            return MockResponse(MOCK_ANTI_FORGERY_RESPONSE, 200, kwargs)

        for pattern, response in routes:
            if pattern in args[0]:
                return MockResponse(response, 200, kwargs)

        return MockResponse("Not Found", 200, kwargs)

    return mocked_requests_get
