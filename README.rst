**********************************
Srp Energy Developer APIs - Python
**********************************
.. image:: https://travis-ci.org/lamoreauxlab/srpenergy-api-client-python.svg?branch=master
    :target: https://travis-ci.org/lamoreauxlab/srpenergy-api-client-python

.. image:: https://coveralls.io/repos/github/lamoreauxlab/srpenergy-api-client-python/badge.svg?branch=master
    :target: https://coveralls.io/github/lamoreauxlab/srpenergy-api-client-python?branch=master

.. image:: https://readthedocs.org/projects/srpenergy-api-client-python/badge/?version=latest
    :target: https://srpenergy-api-client-python.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://requires.io/github/lamoreauxlab/srpenergy-api-client-python/requirements.svg?branch=master
    :target: https://requires.io/github/lamoreauxlab/srpenergy-api-client-python/requirements/?branch=master
    :alt: Requirements Status

.. image:: https://badge.fury.io/py/srpenergy.svg
    :target: https://badge.fury.io/py/srpenergy
    :alt: Latest version on PyPi

.. image:: https://img.shields.io/pypi/pyversions/srpenergy.svg
    :target: https://pypi.org/project/srpenergy/
    :alt: Supported Python versions

The ``srpenergy`` module is an unofficial Python module for interacting with Srp_ Energy data.

- Development: https://github.com/lamoreauxlab/srpenergy-api-client-python/
- Documentation: https://srpenergy-api-client-python.readthedocs.io/

Srp provides an hourly energy usage report for their customers. The ``srpenergy`` module fetches the data found via the api.

The data returned from the hourly url ``https://myaccount.srpnet.com/myaccountapi/api/usage/hourlydetail?billaccount=<code>&beginDate=<MM-DD-YYYY>&endDate=<MM-DD-YYYY>``

.. code-block:: json
    {   "hourlyConsumptionList": [],
        "hourlyGenerationList": [],
        "hourlyReceivedList": [],
        "hourlyUsageList":[{
            {
                "date": "2019-10-09T00:00:00",
                "hour": "2019-10-09T00:00:00",
                "onPeakKwh": 0.0,
                "offPeakKwh": 0.0,
                "shoulderKwh": 0.0,
                "superOffPeakKwh": 0.0,
                "totalKwh": 0.4,
                "onPeakCost": 0.0,
                "offPeakCost": 0.0,
                "shoulderCost": 0.0,
                "superOffPeakCost": 0.0,
                "totalCost": 0.08
            },
            {'...'}
        ],
        "demandList":[]
    }

Installing
==========

It is distributed on PyPI_ and can be installed with pip::

   pip install srpenergy

.. _Srp: https://www.srpnet.com/
.. _PyPI: https://pypi.python.org/pypi/srpenergy

Use
==========

.. code-block:: python

    from srpenergy.client import SrpEnergyClient

    accountid = 'your account id'
    username = 'your username'
    password = 'your password'
    client = SrpEnergyClient(accountid, username, password)
    usage = client.usage(start_date, end_date)
    date, hour, isodate, kwh, cost = usage[0]
