import datetime
import requests

class SrpEnergyClient(object):

    def __init__(self, accountid, username, password):

        # Validate paramters

        self.accountid = accountid
        self.username = username
        self.password = password

    def _strip_currency(self, str):

        return str.replace('$','')

    def _get_iso_time(self, row):

        strDate = datetime.datetime.strptime(row[0], '%m/%d/%Y').strftime('%Y-%m-%d') 
        strTime = datetime.datetime.strptime(row[1], '%I:%M %p').strftime('%H:%M:%S')
        
        return strDate + "T" + strTime + "-7:00"

    def get_usage(self, startdate, enddate):

        # Validate parameters
        if not isinstance(startdate, datetime.datetime):
            raise ValueError("Parameter startdate must be datetime.")

        if not isinstance(enddate, datetime.datetime):
            raise ValueError("Parameter enddate must be datetime.")

        # Validate date ranges
        if startdate > enddate:
            raise ValueError("Parameter startdate can not be greater than enddate.")

        # Validate date ranges
        if startdate > datetime.datetime.now():
            raise ValueError("Parameter startdate can not be greater than now.")

        try:

            # Convert datetime to strings
            str_startdate = startdate.strftime("%m/%d/%Y")
            str_enddate = enddate.strftime("%m/%d/%Y")

            s = requests.session()
        
            result = s.get('https://www.srpnet.com/')
            result = s.post('https://myaccount.srpnet.com/sso/login/loginuser', data = {'UserName' : self.username, 'Password' : self.password})
            result = s.get('https://myaccount.srpnet.com/MyAccount/usage')
            result = s.get('https://myaccount.srpnet.com/MyAccount/Usage/ExportToExcel?billAccount=' + self.accountid + '&viewDataType=KwhUsage&reportOption=Hourly&startDate=' + str_startdate + '&endDate=' + str_enddate + '&displayCost=false')
            
            resultString = result.content.decode("utf-8") 
            rows = resultString.split('\r\n')
            
            usage = []
            for r in rows[1:-1]:
                row = r.split(',')
                values = (row[0], row[1], self._get_iso_time(row), row[2], self._strip_currency(row[3]))
                usage.append(values)

            return usage

        except Exception as ex:
            raise ex
        