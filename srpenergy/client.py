"""Client module.

This module houses the main class used to fetch energy usage.

"""

import datetime
import requests
from bs4 import BeautifulSoup


def strip_currency(val):
    r"""Return a value without a dollary symbol $."""
    return val.replace('$', '')


def get_iso_time(date_part, time_part):
    r"""Combign date and time into an iso datetime."""
    str_date = datetime.datetime.strptime(
        date_part, '%m/%d/%Y').strftime('%Y-%m-%d')
    str_time = datetime.datetime.strptime(
        time_part, '%I:%M %p').strftime('%H:%M:%S')

    return str_date + "T" + str_time + "-7:00"


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

                result = session.get('https://www.srpnet.com/')
                result = session.post(
                    'https://myaccount.srpnet.com/sso/login/loginuser',
                    data={'UserName': self.username, 'Password': self.password}
                    )
                result_string = result.content.decode("utf-8")
                soup = BeautifulSoup(result_string, "html.parser")
                account_select = soup.find(
                    'select', attrs={'name': 'accountNumber'}
                    )

                accounts = []
                for option in account_select.find_all('option'):
                    if option['value'] != 'newAccount':
                        accounts.append(option['value'])

                valid = len(accounts) > 0

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
        base_usage_url = "https://myaccount.srpnet.com/MyAccount/Usage/"

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
            str_startdate = startdate.strftime('%m/%d/%Y')
            str_enddate = enddate.strftime('%m/%d/%Y')

            with requests.Session() as session:

                result = session.get('https://www.srpnet.com/')
                result = session.post(
                    'https://myaccount.srpnet.com/sso/login/loginuser',
                    data={'UserName': self.username, 'Password': self.password}
                    )
                result = session.get(base_usage_url)
                result = session.get(
                    base_usage_url + '/ExportToExcel?billAccount=' +
                    self.accountid +
                    '&viewDataType=KwhUsage&reportOption=Hourly&startDate=' +
                    str_startdate + '&endDate=' + str_enddate +
                    '&displayCost=false')

                rows = result.content.decode('utf-8').split('\r\n')

                if rows[0] == '<!DOCTYPE html>':
                    raise TypeError("Expected csv but received html.")

                usage = []
                for row in rows[1:-1]:
                    s_date, s_time, s_kwh, s_cost, \
                        *peak = row.split(',')  # pylint: disable=W0612
                    values = (
                        s_date,
                        s_time,
                        get_iso_time(s_date, s_time),
                        s_kwh,
                        strip_currency(s_cost))
                    usage.append(values)

                return usage

        except Exception as ex:
            raise ex
