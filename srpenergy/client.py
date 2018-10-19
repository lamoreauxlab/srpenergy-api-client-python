"""Client module.

This module houses the main class used to fetch energy usage.

"""

import datetime
import requests


class SrpEnergyClient(object):
    r"""SrpEnergyClient(accountid, username, password)

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

    def __init__(self, accountid, username, password):

        # Validate paramters

        self.accountid = accountid
        self.username = username
        self.password = password

    def _strip_currency(self, val):

        return val.replace('$', '')

    def _get_iso_time(self, date_part, time_part):

        str_date = datetime.datetime.strptime(
            date_part, '%m/%d/%Y').strftime('%Y-%m-%d')
        str_time = datetime.datetime.strptime(
            time_part, '%I:%M %p').strftime('%H:%M:%S')

        return str_date + "T" + str_time + "-7:00"

    def usage(self, startdate, enddate):
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

                usage = []
                for row in rows[1:-1]:
                    str_date, str_time, str_kwh, str_cost = row.split(',')
                    values = (
                        str_date, str_time, self._get_iso_time(str_date, str_time), str_kwh,
                        self._strip_currency(str_cost))
                    usage.append(values)

                return usage

        except Exception as ex:
            raise ex
