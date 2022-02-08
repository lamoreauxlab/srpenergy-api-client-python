"""Client module.

This module houses the main class used to fetch energy usage.

"""

from datetime import datetime, timedelta
import re
from urllib.parse import unquote

from dateutil.parser import parse
import requests

BASE_USAGE_URL = "https://myaccount.srpnet.com/myaccountapi/api/"


def get_pretty_date(date_part):
    r"""Return a formatted date from an iso date."""
    date = parse(date_part)
    return date.strftime("%m/%d/%Y")


def get_pretty_time(date_part):
    r"""Return a formatted time from an iso date."""
    date = parse(date_part)
    return date.strftime("%H:%M %p")


def get_rate(str_usage_time):
    r"""Return the time of use pricing for the given time.

    From the SRP website
    peak times:
    Winter      Nov-Apr (5am-9am, 5pm-9pm) 9.51 peak, 6.91 offpeak
    Summer      May-Oct (2pm-8pm) 20.94 peak, 7.27 offpeak
    Summer Peak Jul,Aug (2pm-8pm) 24.09, 7.3

    Higher on-peak prices are in effect Monday through Friday
    only during the hours shown.
    Lower off-peak prices are in effect all other weekday hours,
    weekends and six observed holidays:
    New Year's Day, Memorial Day, Independence Day,
    Labor Day, Thanksgiving Day and Christmas Day.

    see https://srpnet.com/prices/pdfx/April2015/E-26.pdf
    """
    # Validate parameters
    if str_usage_time is None:
        raise TypeError("Parameter str_usage_time can not be none.")

    try:
        usage_time = parse(str_usage_time)
    except ValueError as error:
        raise ValueError(
            "Parameter str_usage_time should be parsed as a datetime."
        ) from error

    summer_start_date = datetime(usage_time.year, 5, 1, 0, 0, 0)
    summer_end_date = datetime(usage_time.year, 11, 1, 0, 0, 0) - timedelta(seconds=1)

    peak_summer_start_date = datetime(usage_time.year, 7, 1, 0, 0, 0)
    peak_summer_end_date = datetime(usage_time.year, 9, 1, 0, 0, 0) - timedelta(
        seconds=1
    )

    week_day_idx = usage_time.weekday()

    # Holidays (New Years, Independence, Memorial, Labor, Thanks, Christmas)
    is_holiday = usage_time.month == 1 and usage_time.day == 1
    is_holiday = is_holiday or (usage_time.day == 4 and usage_time.month == 7)
    is_holiday = is_holiday or (
        usage_time.month == 5 and (week_day_idx == 0 and (31 - usage_time.day) < 7)
    )
    is_holiday = is_holiday or (
        usage_time.month == 9 and (week_day_idx == 0 and (usage_time.day <= 7))
    )
    is_holiday = is_holiday or (usage_time.month == 11 and week_day_idx == 3)
    is_holiday = is_holiday or (usage_time.month == 12 and usage_time.day == 24)

    is_weekend = week_day_idx > 4

    if peak_summer_start_date <= usage_time <= peak_summer_end_date:
        # Check if is Peak Summer

        is_peak = 14 <= usage_time.hour < 20
        peak_rate = 0.2409
        non_peak_rate = 0.073

    elif summer_start_date <= usage_time <= summer_end_date:
        # Check if regular Summer

        # Is peak time
        is_peak = 14 <= usage_time.hour < 20
        peak_rate = 0.2094
        non_peak_rate = 0.0727

    else:
        # Must be winter

        # Check if in Peak hours
        is_peak = 5 <= usage_time.hour < 9 or 17 <= usage_time.hour < 21

        peak_rate = 0.0951
        non_peak_rate = 0.0691

    is_peak = is_peak and not is_holiday and not is_weekend
    if is_peak:
        rate = peak_rate
    else:
        rate = non_peak_rate

    return rate, is_peak


class SrpEnergyClient:
    r"""SrpEnergyClient(accountid, username, password).

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

    def __init__(self, accountid, username, password):  # noqa: D107

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

    def validate(self):
        r"""Validate user credentials.

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

                response = session.post(
                    BASE_USAGE_URL + "/login/authorize",
                    data={"username": self.username, "password": self.password},
                )
                data = response.json()

                valid = data["message"] == "Log in successful."

                return valid

        except Exception:  # pylint: disable=W0703
            return False

    def usage(self, startdate, enddate, is_tou=False):  # pylint: disable=R0914
        r"""Get the energy usage for a given date range.

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

            # Convert datetime to strings
            str_startdate = startdate.strftime("%m-%d-%Y")
            str_enddate = enddate.strftime("%m-%d-%Y")

            with requests.Session() as session:

                response = session.post(
                    BASE_USAGE_URL + "login/authorize",
                    data={"username": self.username, "password": self.password},
                )

                response = session.get(BASE_USAGE_URL + "login/antiforgerytoken")
                xsrf_token = unquote(response.cookies["xsrf-token"])

                response = session.get(
                    BASE_USAGE_URL
                    + "usage/hourlydetail?billaccount="
                    + self.accountid
                    + "&beginDate="
                    + str_startdate
                    + "&endDate="
                    + str_enddate,
                    headers={"x-xsrf-token": xsrf_token},
                )

                data = response.json()
                hourly_usage_list = data["hourlyUsageList"]

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

                    # Check if on Time of Use Plan
                    if is_tou:

                        rate, is_peak = get_rate(row["date"])

                        if is_peak:
                            total_kwh = row["onPeakKwh"]
                        else:
                            total_kwh = row["offPeakKwh"]

                        total_cost = total_kwh * rate

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
