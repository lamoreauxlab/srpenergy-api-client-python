"""Client module.

This module houses the main class used to fetch energy usage.

"""

from datetime import datetime, timedelta
import re
from urllib.parse import unquote

from dateutil.parser import parse
import requests

BASE_USAGE_URL = "https://myaccount.srpnet.com/myaccountapi/api/"

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": BASE_USAGE_URL,
}
HTTP_FORBIDDEN_ERROR = 403

def get_pretty_date(date_part):
    """Return a formatted date from an iso date."""
    date = parse(date_part)
    return date.strftime("%m/%d/%Y")


def get_pretty_time(date_part):
    """Return a formatted time from an iso date."""
    date = parse(date_part)
    return date.strftime("%H:%M %p")


class SrpEnergyError(Exception):
    """Raised when the SRP API returns an unexpected response."""


class SrpEnergyClient:
    """SrpEnergyClient(accountid, username, password).

    Client used to fetch srp energy usage.

    Parameters
    ----------
    accountid : string
        An srp account id.
    username: string
        An srp account username.
    password: string
        An srp account password

    Methods
    -------
    validate()
        Validate user credentials.
    usage(startdate, enddate)
        Get the usage for a given date range.

    """

    def __init__(self, accountid, username, password):

        # Validate parameters
        if accountid is None:
            raise TypeError("Parameter account can not be none.")

        if username is None:
            raise TypeError("Parameter username can not be none.")

        if password is None:
            raise TypeError("Parameter password can not be none.")

        if not accountid:
            raise ValueError("Parameter accountid must have length greater than 0.")

        if not username:
            raise ValueError("Parameter username must have length greater than 0.")

        if not password:
            raise ValueError("Parameter password must have length greater than 0.")

        if not re.match(r"^\d{9}$", accountid):
            raise ValueError("Parameter account should only contain numbers.")

        self.accountid = accountid
        self.username = username
        self.password = password

    def _check_response(self, response: requests.Response, step: str) -> None:
        """Raise a clear error if a response indicates failure."""
        if response.status_code == HTTP_FORBIDDEN_ERROR:
            # Cloudflare or SRP access control blocked the request
            raise SrpEnergyError(
                f"Access denied (403) during '{step}'. "
                "SRP's site may be blocking automated requests. "
                f"Ray ID may be present in response: {response.text[:200]}"
            )
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise SrpEnergyError(
                f"HTTP error during '{step}': {e} — body: {response.text[:200]}"
            ) from e

    def validate(self):
        """Validate user credentials.

        Returns
        -------
        bool

        Examples
        --------
        Validate credentials.

        >>> from srpenergy.client import SrpEnergyClient
        >>>
        >>> accountid = 'your account id'
        >>> username = 'your username'
        >>> password = 'your password'
        >>> client = SrpEnergyClient(accountid, username, password)
        >>>
        >>> valid = client.validate()
        >>> print(valid)
        True

        """
        try:
            with requests.Session() as session:
                session.headers.update(BROWSER_HEADERS)

                # Step 1: Authenticate
                response = session.post(
                    BASE_USAGE_URL + "/login/authorize",
                    data={"username": self.username, "password": self.password},
                )
                self._check_response(response, "login/authorize")
                data = response.json()

                return data["message"] == "Log in successful."

        except Exception:  # pylint: disable=W0703
            return False

    def usage(self, startdate, enddate, is_tou=False):  # pylint: disable=R0914
        """Get the energy usage for a given date range.

        Parameters
        ----------
        startdate : datetime
            the start date
        enddate : datetime
            the end date
        is_tou : bool
            indicate if usage is a time of use plan

        Returns
        -------
        list of tuple
            In the form of (datepart, timepart, isotime, kw, cost)

        Raises
        ------
        ValueError
            If ``startdate`` or ``enddate`` are not datetime,
            or if ``startdate`` is greater than ``enddate``,
            or if ``startdate`` is greater than now.

        Examples
        --------
        Get the hourly usage for a given day.

        >>> from srpenergy.client import SrpEnergyClient
        >>> accountid = 'your account id'
        >>> username = 'your username'
        >>> password = 'your password'
        >>> client = SrpEnergyClient(accountid, username, password)
        >>> start_date = datetime(2018, 9, 19, 0, 0, 0)
        >>> end_date = datetime(2018, 9, 19, 23, 0, 0)
        >>> usage = client.usage(start_date, end_date)
        >>> print(usage)
        [
        ('9/19/2018', '12:00 AM', '2018-09-19T00:00:00-7:00', '1.2', '0.17'),
        ('9/19/2018', '1:00 AM', '2018-09-19T01:00:00-7:00', '2.1', '0.30'),
        ('9/19/2018', '2:00 AM', '2018-09-19T02:00:00-7:00', '1.5', '0.23'),
        ...
        ('9/19/2018', '9:00 PM', '2018-09-19T21:00:00-7:00', '1.2', '0.19'),
        ('9/19/2018', '10:00 PM', '2018-09-19T22:00:00-7:00', '1.1', '0.18'),
        ('9/19/2018', '11:00 PM', '2018-09-19T23:00:00-7:00', '0.4', '0.09')
        ]

        """
        # Validate parameters
        if not isinstance(startdate, datetime):
            raise ValueError("Parameter startdate must be datetime.")

        if not isinstance(enddate, datetime):
            raise ValueError("Parameter enddate must be datetime.")

        # Validate date ranges
        if startdate > enddate:
            raise ValueError("Parameter startdate can not be greater than enddate.")

        # Validate date ranges
        if startdate.timestamp() > datetime.now().timestamp():
            raise ValueError("Parameter startdate can not be greater than now.")

        try:
            hourly_usage_list = self._fetch_hourly_rows(startdate, enddate)

            usage = []
            for row in hourly_usage_list:
                total_kwh = row["totalKwh"]
                if total_kwh == 0:
                    # Build the total_kwh from separate fields for EZ-3.
                    total_kwh = (
                        row["onPeakKwh"]
                        + row["offPeakKwh"]
                        + row["shoulderKwh"]
                        + row["superOffPeakKwh"]
                    )

                total_cost = row["totalCost"]
                if total_cost == 0:
                    # Build the total_cost from separate fields for EZ-3.
                    total_cost = (
                        row["onPeakCost"]
                        + row["offPeakCost"]
                        + row["shoulderCost"]
                        + row["superOffPeakCost"]
                    )

                values = (
                    get_pretty_date(row["date"]),
                    get_pretty_time(row["date"]),
                    row["date"],
                    total_kwh,
                    round(total_cost, 2),
                )
                usage.append(values)

            return usage

        except Exception as ex:
            raise ex

    def _fetch_hourly_rows(self, startdate, enddate):
        """Authenticate and fetch raw hourly usage rows from the SRP API.

        Returns
        -------
        list of dict
            Raw ``hourlyUsageList`` rows exactly as SRP's API returns them,
            each containing onPeakKwh/offPeakKwh/shoulderKwh/superOffPeakKwh
            and their cost equivalents, plus totalKwh/totalCost.

        Shared by both ``usage()`` (which collapses each row to a single
        total) and ``usage_detailed()`` (which preserves the per-tariff-bucket
        breakdown), so the login/session flow is implemented once.
        """
        str_startdate = startdate.strftime("%m-%d-%Y")
        str_enddate = enddate.strftime("%m-%d-%Y")

        with requests.Session() as session:
            session.headers.update(BROWSER_HEADERS)

            # Step 1: Authenticate
            response = session.post(
                BASE_USAGE_URL + "login/authorize",
                data={"username": self.username, "password": self.password},
            )
            self._check_response(response, "login/authorize")

            # Step 2: Fetch XSRF token
            response = session.get(BASE_USAGE_URL + "login/antiforgerytoken")

            if "xsrf-token" not in response.cookies:
                raise SrpEnergyError(
                    "XSRF token cookie missing after antiforgerytoken request. "
                    f"Cookies received: {list(response.cookies.keys())}"
                )

            xsrf_token = unquote(response.cookies["xsrf-token"])

            # Step 3: Fetch usage data
            response = session.get(
                BASE_USAGE_URL + "usage/hourlydetail",
                params={
                    "billaccount": self.accountid,
                    "beginDate": str_startdate,
                    "endDate": str_enddate,
                },
                headers={"x-xsrf-token": xsrf_token},
            )

            self._check_response(response, "usage/hourlydetail")

            data = response.json()
            return data["hourlyUsageList"]

    def usage_detailed(self, startdate, enddate):
        """Get hourly energy usage broken out by Time-of-Use tariff bucket.

        Unlike ``usage()``, which collapses each hour to a single combined
        kwh/cost figure, this preserves the on-peak/off-peak/shoulder/
        super-off-peak breakdown as returned by SRP's API. For non-TOU
        accounts, the four bucket fields will be 0 and ``total_kwh``/
        ``total_cost`` will carry the real value instead.

        Parameters
        ----------
        startdate : datetime
            the start date
        enddate : datetime
            the end date

        Returns
        -------
        list of dict
            Each dict has keys: date, time, iso_date, on_peak_kwh,
            off_peak_kwh, shoulder_kwh, super_off_peak_kwh, total_kwh,
            on_peak_cost, off_peak_cost, shoulder_cost, super_off_peak_cost,
            total_cost.

        Raises
        ------
        ValueError
            If ``startdate`` or ``enddate`` are not datetime,
            or if ``startdate`` is greater than ``enddate``,
            or if ``startdate`` is greater than now.
        """
        if not isinstance(startdate, datetime):
            raise ValueError("Parameter startdate must be datetime.")

        if not isinstance(enddate, datetime):
            raise ValueError("Parameter enddate must be datetime.")

        if startdate > enddate:
            raise ValueError("Parameter startdate can not be greater than enddate.")

        if startdate.timestamp() > datetime.now().timestamp():
            raise ValueError("Parameter startdate can not be greater than now.")

        try:
            hourly_usage_list = self._fetch_hourly_rows(startdate, enddate)

            usage = []
            for row in hourly_usage_list:
                total_kwh = row["totalKwh"]
                if total_kwh == 0:
                    total_kwh = (
                        row["onPeakKwh"]
                        + row["offPeakKwh"]
                        + row["shoulderKwh"]
                        + row["superOffPeakKwh"]
                    )

                total_cost = row["totalCost"]
                if total_cost == 0:
                    total_cost = (
                        row["onPeakCost"]
                        + row["offPeakCost"]
                        + row["shoulderCost"]
                        + row["superOffPeakCost"]
                    )

                usage.append(
                    {
                        "date": get_pretty_date(row["date"]),
                        "time": get_pretty_time(row["date"]),
                        "iso_date": row["date"],
                        "on_peak_kwh": row["onPeakKwh"],
                        "off_peak_kwh": row["offPeakKwh"],
                        "shoulder_kwh": row["shoulderKwh"],
                        "super_off_peak_kwh": row["superOffPeakKwh"],
                        "total_kwh": total_kwh,
                        "on_peak_cost": round(row["onPeakCost"], 2),
                        "off_peak_cost": round(row["offPeakCost"], 2),
                        "shoulder_cost": round(row["shoulderCost"], 2),
                        "super_off_peak_cost": round(row["superOffPeakCost"], 2),
                        "total_cost": round(total_cost, 2),
                    }
                )

            return usage

        except Exception as ex:
            raise ex
