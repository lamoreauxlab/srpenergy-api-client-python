=========================
API Documentation
=========================

This is an unofficial documentation of the SRP Energy Usage api. Srp provides an hourly energy usage report for their customers.

There are three steps to fetch the data:

1. Log into the site with user credentials.
2. Request an xsrf-token token.
3. Request the usage data.


Log into site
-------------

Post x-www-form-urlencoded parameters to the endpoint.

username
    The username for the account.

password
    The password for the account.

.. code-block:: bash

    # Post to
    https://myaccount.srpnet.com/myaccountapi/api/login/authorize

    # Include x-www-form-urlencoded parameters
    # username=<username>
    # password=<password>

Fetch Xsrf token
----------------

Then fetch the xsrf-token by calling:

.. code-block:: bash

    # Get
    https://myaccount.srpnet.com/myaccountapi/api/login/authorize

    # Save the result of the xsrf-token cookie

Call Usage data
---------------

Finally call the usage endpoint ad include the following:

code
    billing account number

str_startdate
    start date of billing usage in the format MM-DD-YYYY

str_enddate
    end date of billing usage in the format MM-DD-YYYY

xsrf-token
    the xsrf-token used in the header



.. code-block::

    https://myaccount.srpnet.com/myaccountapi/api/usage/hourlydetail?billaccount="
                    + <code>
                    + "&beginDate="
                    + <str_startdate>
                    + "&endDate="
                    + str_enddate,

    # Headers
    # "x-xsrf-token": xsrf_token_value

Results
-------

.. code-block:: JSON

    {   "hourlyConsumptionList": [],
        "hourlyGenerationList": [],
        "hourlyReceivedList": [],
        "hourlyUsageList":[{
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
            }
        ],
        "demandList":[]
    }

.. note::
    Time of use customers do not receive a ``totalKwh`` or ``totalCost`` from the api. These values are calculated from ``onPeakKwh``, ``offPeakKwh``, and the fomula defined by the SRP `TOU price plan sheet <https://srpnet.com/prices/pdfx/April2015/E-26.pdf>`_

    EZ3 customers show 0.0 for ``totalKwh`` and ``totalCost``. The values are split between ``onPeak``, ``offPeak``, ``shoulder``, and ``superOffPeak``.
