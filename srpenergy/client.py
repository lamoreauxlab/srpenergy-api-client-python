"""Client module.

This module houses the main class used to fetch energy usage.

"""

import datetime
from dateutil.parser import parse
import requests


BASE_USAGE_URL = 'https://myaccount.srpnet.com/myaccountapi/api/'


def get_pretty_date(date_part):
    r"""Return a formated date from an iso date."""
    date = parse(date_part)
    return date.strftime('%m/%d/%Y')


def get_pretty_time(date_part):
    r"""Return a formated time from an iso date."""
    date = parse(date_part)
    return date.strftime('%H:%M %p')


class SrpEnergyClient():
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
            raise ValueError(
                "Parameter accountid must have length greater than 0.")

        if not username:
            raise ValueError(
                "Parameter username must have length greater than 0.")

        if not password:
            raise ValueError(
                "Parameter password must have length greater than 0.")

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
                    BASE_USAGE_URL + '/login/authorize',
                    data={'username': self.username, 'password': self.password}
                    )
                data = response.json()

                valid = data['message'] == 'Log in successful.'

                return valid

        except Exception:  # pylint: disable=W0703
            return False

    def usage(self, startdate, enddate):  # pylint: disable=R0914
        r"""Get the energy usage for a given date range.

        Parameters
        ----------
        startdate : datetime
            the start date
        enddate : datetime
            the end date

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
        if not isinstance(startdate, datetime.datetime):
            raise ValueError("Parameter startdate must be datetime.")

        if not isinstance(enddate, datetime.datetime):
            raise ValueError("Parameter enddate must be datetime.")

        # Validate date ranges
        if startdate > enddate:
            raise ValueError(
                "Parameter startdate can not be greater than enddate.")

        # Validate date ranges
        if startdate > datetime.datetime.now():
            raise ValueError(
                "Parameter startdate can not be greater than now.")

        try:

            # Convert datetime to strings
            str_startdate = startdate.strftime('%m-%d-%Y')
            str_enddate = enddate.strftime('%m-%d-%Y')

            with requests.Session() as session:

                response = session.post(
                    BASE_USAGE_URL + 'login/authorize',
                    data={'username': self.username, 'password': self.password}
                    )

                response = session.get('login/antiforgerytoken')
                data = response.json()
                xsrf_token = data['xsrfToken']

                response = session.get(
                    BASE_USAGE_URL + 'usage/hourlydetail?billaccount=' +
                    self.accountid +
                    '&beginDate=' + str_startdate + '&endDate=' + str_enddate,
                    headerheaders={"x-xsrf-token": xsrf_token})

                data = response.json()
                hourly_usage_list = data['hourlyUsageList']

                usage = []
                for row in hourly_usage_list:
                    values = (
                        get_pretty_date(row['date']),
                        get_pretty_time(row['date']),
                        row['date'],
                        row['totalKwh'],
                        row['totalCost'])
                    usage.append(values)

                return usage

        except Exception as ex:
            raise ex
