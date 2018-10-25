import os
import unittest
from srpenergy.client import SrpEnergyClient
from datetime import datetime, timedelta


class TestGetUsage(unittest.TestCase):

    def setUp(self):

        self.accountid = os.environ.get('SRPENERGY_ACCOUNT_ID')
        self.username = os.environ.get('SRPENERGY_USERNAME')
        self.password = os.environ.get('SRPENERGY_PASSWORD')

    def test_hasAccountId(self):
        self.assertTrue('SRPENERGY_ACCOUNT_ID' in os.environ)

    def test_getEnvironment(self):
        self.assertIsNotNone(self.accountid)

    def test_badParameterStartDateString(self):

        end_date = datetime(2018, 10, 5, 12, 0, 0)

        client = SrpEnergyClient(self.accountid, self.username, self.password)

        with self.assertRaises(ValueError):
            client.usage('20181001', end_date)

    def test_badParameterEndDateString(self):

        start_date = datetime(2018, 10, 5, 12, 0, 0)

        client = SrpEnergyClient(self.accountid, self.username, self.password)

        with self.assertRaises(ValueError):
            client.usage(start_date, '20181001')

    def test_badParameterStartDateAfterNow(self):

        start_date = datetime.now() + timedelta(days=10)
        end_date = datetime(2018, 10, 5, 12, 0, 0)

        client = SrpEnergyClient(self.accountid, self.username, self.password)

        with self.assertRaises(ValueError):
            client.usage(start_date, end_date)

    def test_badParameterStartDateAfterEndDate(self):

        start_date = datetime(2018, 10, 6, 12, 0, 0)
        end_date = datetime(2018, 10, 5, 12, 0, 0)

        client = SrpEnergyClient(self.accountid, self.username, self.password)

        with self.assertRaises(ValueError):
            client.usage(start_date, end_date)

    def test_getUsage(self):

        start_date = datetime(2018, 10, 1, 6, 0, 0)
        end_date = datetime(2018, 10, 5, 12, 0, 0)
        client = SrpEnergyClient(self.accountid, self.username, self.password)

        usage = client.usage(start_date, end_date)

        self.assertEqual(len(usage), 120)

    def test_singlDayUsageKw(self):

        start_date = datetime(2018, 9, 19, 0, 0, 0)
        end_date = datetime(2018, 9, 19, 23, 0, 0)
        client = SrpEnergyClient(self.accountid, self.username, self.password)

        usage = client.usage(start_date, end_date)

        self.assertEqual(len(usage), 24)

        date, hour, isodate, kwh, cost = usage[0]

        self.assertEqual(kwh, '1.2')
        self.assertEqual(cost, '0.17')

    def test_latestDayUsageKw(self):

        start_date = datetime(2018, 9, 19, 0, 0, 0)
        end_date = datetime(2018, 9, 19, 23, 0, 0)
        client = SrpEnergyClient(self.accountid, self.username, self.password)

        usage = client.usage(start_date, end_date)

        self.assertEqual(len(usage), 24)

        date, hour, isodate, kwh, cost = usage[-1]

        self.assertEqual(kwh, '0.4')
        self.assertEqual(cost, '0.09')

    def test_none_accountid(self):
        
        with self.assertRaises(TypeError):
            client = SrpEnergyClient(None, 'b', 'c')

    def test_none_username(self):
        
        with self.assertRaises(TypeError):
            client = SrpEnergyClient('a', None, 'c')
    
    def test_none_password(self):

        with self.assertRaises(TypeError):
            client = SrpEnergyClient('a', 'b', None)

    def test_blank_accountid(self):

        with self.assertRaises(ValueError):
            client = SrpEnergyClient('', 'b', 'c')
    
    def test_blank_username(self):

        with self.assertRaises(ValueError):
             client = SrpEnergyClient('a', '', 'c')

    def test_blank_password(self):

        with self.assertRaises(ValueError):
            client = SrpEnergyClient('a', 'b', '')

    def test_bad_crendentials(self):

        start_date = datetime(2018, 9, 19, 0, 0, 0)
        end_date = datetime(2018, 9, 19, 23, 0, 0)
        client = SrpEnergyClient('a', 'b', 'c')

        with self.assertRaises(TypeError):
            client.usage(start_date, end_date)