"""The tests for the Srp Energy API Time of Use cases."""
from datetime import datetime
from unittest.mock import patch

from srpenergy.client import SrpEnergyClient

from tests.common import (
    MOCK_LOGIN_RESPONSE,
    PATCH_GET,
    PATCH_POST,
    TEST_PASSWORD,
    TEST_USER_NAME,
    get_mock_requests,
)

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

MOCK_USAGE_TOU_GENERAL_RESPONSE = {
    "hourlyUsageList": [
        {
            "date": "2020-06-28T00:00:00",
            "hour": "2020-06-28T00:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 4.0,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2020-06-28T01:00:00",
            "hour": "2020-06-28T01:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 5.4,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2020-06-28T02:00:00",
            "hour": "2020-06-28T02:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 5.0,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2020-06-28T03:00:00",
            "hour": "2020-06-28T03:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 4.8,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2020-06-28T04:00:00",
            "hour": "2020-06-28T04:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 3.2,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2020-06-28T05:00:00",
            "hour": "2020-06-28T05:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 2.5,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2020-06-28T06:00:00",
            "hour": "2020-06-28T06:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 3.0,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2020-06-28T07:00:00",
            "hour": "2020-06-28T07:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 2.8,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2020-06-28T08:00:00",
            "hour": "2020-06-28T08:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 3.6,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2020-06-28T09:00:00",
            "hour": "2020-06-28T09:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 3.9,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2020-06-28T10:00:00",
            "hour": "2020-06-28T10:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 4.0,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2020-06-28T11:00:00",
            "hour": "2020-06-28T11:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 4.6,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2020-06-28T12:00:00",
            "hour": "2020-06-28T12:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 6.5,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2020-06-28T13:00:00",
            "hour": "2020-06-28T13:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 9.2,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2020-06-28T14:00:00",
            "hour": "2020-06-28T14:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 9.0,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2020-06-28T15:00:00",
            "hour": "2020-06-28T15:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 7.2,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2020-06-28T16:00:00",
            "hour": "2020-06-28T16:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 6.0,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2020-06-28T17:00:00",
            "hour": "2020-06-28T17:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 9.1,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2020-06-28T18:00:00",
            "hour": "2020-06-28T18:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 7.0,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2020-06-28T19:00:00",
            "hour": "2020-06-28T19:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 5.9,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2020-06-28T20:00:00",
            "hour": "2020-06-28T20:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 4.5,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2020-06-28T21:00:00",
            "hour": "2020-06-28T21:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 4.1,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2020-06-28T22:00:00",
            "hour": "2020-06-28T22:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 3.7,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
        {
            "date": "2020-06-28T23:00:00",
            "hour": "2020-06-28T23:00:00",
            "onPeakKwh": 0.0,
            "offPeakKwh": 4.0,
            "shoulderKwh": 0.0,
            "superOffPeakKwh": 0.0,
            "totalKwh": 0.0,
            "onPeakCost": 0.0,
            "offPeakCost": 0.0,
            "shoulderCost": 0.0,
            "superOffPeakCost": 0.0,
            "totalCost": 0.0,
        },
    ]
}


ROUTES = [
    ("06-24-2020", MOCK_USAGE_TOU_SUMMER_OFF_PEAK_RESPONSE),
    ("06-25-2020", MOCK_USAGE_TOU_SUMMER_ON_PEAK_RESPONSE),
    ("07-24-2019", MOCK_USAGE_TOU_PEAK_SUMMER_OFF_PEAK_RESPONSE),
    ("07-23-2019", MOCK_USAGE_TOU_PEAK_SUMMER_ON_PEAK_RESPONSE),
    ("12-20-2019", MOCK_USAGE_TOU_WINTER_OFF_PEAK_RESPONSE),
    ("12-19-2019", MOCK_USAGE_TOU_WINTER_ON_PEAK_RESPONSE),
    ("06-28-2020", MOCK_USAGE_TOU_GENERAL_RESPONSE),
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


def test_daily_aggregation_tou():
    """Test that hourly roll up matches SRP Daily."""
    # "dailyReadList": [{
    #             "day": "2018-06-28T07:00:00Z",
    #             "date": "2018-06-28T07:00:00Z",
    #             "meterReadDate": "2018-06-29T00:00:00-07:00",
    #             "superOffPeakKwh": 0.0,
    #             "shoulderKwh": 0.0,
    #             "offPeakKwh": 61.0,
    #             "onPeakKwh": 39.0,
    #             "totalKwh": 0.0,
    #             "onPeakCost": 9.33,
    #             "offPeakCost": 5.51,
    #             "shoulderCost": 0.0,
    #             "superOffPeakCost": 0.0,
    #             "totalCost": 0.0,
    #             "dailyCost": 14.84
    #         }

    with patch(PATCH_GET) as session_get, patch(PATCH_POST) as session_post:
        session_post.return_value = MOCK_LOGIN_RESPONSE
        session_get.side_effect = get_mock_requests(ROUTES)

        client = SrpEnergyClient(TEST_ACCOUNT_TOU_ID, TEST_USER_NAME, TEST_PASSWORD)

        start_date = datetime(2020, 6, 28, 0, 0, 0)
        end_date = datetime(2020, 6, 28, 23, 0, 0)

        usage = client.usage(start_date, end_date, True)

        total_kwh = 0
        total_cost = 0
        for line in usage:
            _date, _hour, _isodate, kwh, cost = line
            total_kwh = total_kwh + kwh
            total_cost = total_cost + cost

        assert len(usage) == 24
        assert total_kwh == 123
        assert total_cost == 8.92
