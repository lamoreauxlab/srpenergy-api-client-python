"""Shared methods and const for tests."""

import json
from unittest.mock import Mock

import requests

PATCH_GET = "srpenergy.client.requests.Session.get"
PATCH_POST = "srpenergy.client.requests.Session.post"

TEST_USER_NAME = "abba"
TEST_PASSWORD = "dabba"  # noqa: S105

MOCK_LOGIN_RESPONSE = Mock()
MOCK_LOGIN_RESPONSE.json.return_value = {
    "message": "Log in successful.",
    "username": "user@example.com",
    "email": "user@example.com",
    "isIrrigator": False,
    "redirectUrl": "",
}
MOCK_CLOUDFLARE_RESPONSE_TEXT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex, nofollow" />
    <title>Access Denied</title>
    <style>
        body {
            background-color: #004B87;
            color: black;
            font-family: Arial, sans-serif;
            text-align: center;
            padding-top: 50px;
        }
        .logo {
            width: 200px;
        }
        .container {
            max-width: 600px;
            margin: auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
        }
        h1 {
            font-size: 2em;
        }
    </style>
\n</head>
<body>
    <div class="container">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 98.37 54.02" width="198.37" height="154.02">
            <rect width="98.37" height="54.02" fill="none"/>
            <g fill="#125590">
                <path d="M28.51,18c0.06,0,0.62,0,0.62,0l9.64,3.9l-0.8,2.95H21.49C20.61,21.64,24.04,18,28.51,18z"/>
                <polygon points="32.22,18 39.86,18 39.09,20.79"/>
                <path d="M21.76,26.01h12.85c1.99,1.38,2.86,3.76,2.22,5.79c-1.17,3.7-5.42,4.19-5.98,4.19c0,0-9.34,0-12.81,0l1.78-6.41h5.4c0.04,0-1.39-0.8-2.26-1.76C22.21,26.99,21.76,26.01,21.76,26.01z"/>
                <polygon points="46.1,24.84 39.42,24.84 40.1,22.45"/>
                <polygon points="40.42,21.33 46.64,23.84 41.21,18.43"/>
                <polygon points="42.4,18 45.87,18 47.58,23.17"/>
                <polygon points="47.09,18 48.75,23.01 50.43,18"/>
                <path d="M44.31,36h-7.98l2.75-9.99h17.41c0,0-0.43,0.95-1.01,1.48c-0.94,0.86-2.12,1.25-2.12,1.25l1.85,5.67l2.34-8.4H74.9c0,0-0.26,1.11-1.7,2.18c-1.58,1.17-3.85,1.6-4.91,1.6h-3.45l-0.52-1.89L62.07,36H48.29l-2.03-7L44.31,36z"/>
                <path d="M51.4,24.84H57c0,0,0.12-0.57,0.15-1.16c0.02-0.58-0.04-1.13-0.04-1.13L51.4,24.84z"/>
                <path d="M49.71,23.29l4.52-4.5c0,0-0.62-0.39-1.2-0.54C52.44,18.1,51.46,18,51.46,18L49.71,23.29z"/>
                <path d="M55.22,19.42l-4.39,4.39l5.9-2.37c0,0-0.23-0.59-0.65-1.13C55.75,19.87,55.22,19.42,55.22,19.42z"/>
                <polygon points="59.77,18 65.21,18 59.09,20.48"/>
                <path d="M57.87,24.84l0.81-2.93L68.35,18h1.27c1.01,0,3.42,0.55,4.96,2.96c1.27,1.97,0.78,3.88,0.68,3.88H57.87z"/>
                <path d="M76.02,20.42c0-1.19,0.97-2.15,2.17-2.15c1.19,0,2.15,0.97,2.15,2.15c0,1.19-0.97,2.17-2.15,2.17C76.99,22.59,76.02,21.62,76.02,20.42z M80.07,20.42c0-1.05-0.84-1.89-1.89-1.89c-1.06,0-1.9,0.84-1.9,1.89c0,1.06,0.84,1.9,1.9,1.9C79.23,22.32,80.07,21.48,80.07,20.42z"/>
                <path d="M79.11,19.9c0-0.37-0.2-0.6-0.8-0.6h-0.99v2.26h0.26v-1.04h0.53l0.65,1.04h0.33l-0.68-1.04C78.8,20.51,79.11,20.35,79.11,19.9z M78.02,20.27h-0.44v-0.7h0.67c0.28,0,0.61,0.04,0.61,0.34C78.85,20.32,78.34,20.27,78.02,20.27z"/>
            </g>
        </svg>

        <h1>Access Denied</h1>
        <p>You are not authorized to access this webpage.</p>
        <p>If you believe this is an error, please reach out to your administrator or SRP contact.</p>

        <p><strong>Ray ID:</strong>omitted</p>
        <p><strong>Your IP:</strong>omitted</p>
    </div>
</body>
</html>
"""


MOCK_ANTI_FORGERY_RESPONSE = {"message": "Success"}

MOCK_ANTI_FORGERY_RESPONSE_COOKIES = {
    "xsrf-token": "CfDJ8KUcoIlbMHV_NbT4uDyb-XA2%7C207f"
}

EXPECTED_WINTER_OFF_PEAK_RATE = 0.0691
EXPECTED_WINTER_ON_PEAK_RATE = 0.0951
EXPECTED_SUMMER_OFF_PEAK_RATE = 0.0727
EXPECTED_SUMMER_ON_PEAK_RATE = 0.2094
EXPECTED_PEAK_SUMMER_OFF_PEAK = 0.073
EXPECTED_PEAK_SUMMER_ON_PEAK = 0.2409
EXPECTED_WINTER_WEEKEND_RATE = 0.0691
EXPECTED_SUMMER_WEEKEND_RATE = 0.0727
EXPECTED_PEAK_SUMMER_WEEKEND_RATE = 0.073

HTTP_RESPONSE_CODE_CLIENT_ERROR = 400


# pylint: disable=R0903
class MockResponse:
    """Mock Response."""

    def __init__(self, json_data, status_code, cookies, kwargs):
        """Create Mock Response."""
        self.json_data = json_data
        self.status_code = status_code
        self.cookies = cookies
        self.kwargs = kwargs
        self.text = (
            json.dumps(json_data) if isinstance(json_data, dict) else str(json_data)
        )

    def json(self):
        """Return mock json."""
        return self.json_data

    def raise_for_status(self):
        """Raise HTTPError if the status code indicates an error."""
        if self.status_code >= HTTP_RESPONSE_CODE_CLIENT_ERROR:
            raise requests.HTTPError(f"HTTP Error: {self.status_code}")


def get_mock_requests(routes, antiforgery_status=200, antiforgery_cookies=None):
    """Return a mock side_effect for requests.get.

    Each route is a (pattern, response) tuple. The pattern is matched against:
      - The request URL
      - The 'beginDate' query param (if present)
      - The 'billaccount' query param (if present)

    Args:
        routes: List of (pattern, response) tuples.
        antiforgery_status: HTTP status code to return for the antiforgery request (default 200).
        antiforgery_cookies: Cookies to return for the antiforgery request.
                             Defaults to MOCK_ANTI_FORGERY_RESPONSE_COOKIES.
                             Pass {} to simulate missing xsrf-token.
    """

    def mocked_requests_get(*args, **kwargs):
        url = args[0] if args else ""

        if "login/antiforgerytoken" in url:
            cookies = (
                antiforgery_cookies
                if antiforgery_cookies is not None
                else MOCK_ANTI_FORGERY_RESPONSE_COOKIES
            )

            return MockResponse(
                MOCK_ANTI_FORGERY_RESPONSE,
                antiforgery_status,
                cookies,
                kwargs,
            )

        params = kwargs.get("params") or {}
        begin_date = params.get("beginDate")
        bill_account = params.get("billaccount", "")

        for pattern, response in routes:
            if pattern in url or pattern in begin_date or pattern in bill_account:
                return MockResponse(response, 200, {}, kwargs)

        raise ValueError(
            f"No mock response matched url='{url}', beginDate='{begin_date}', "
            f"billaccount='{bill_account}'. "
            f"Registered patterns: {[p for p, _ in routes]}"
        )

    return mocked_requests_get
