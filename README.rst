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

.. note:: Time of use customers do not receive a ``totalKwh`` or ``totalCost`` from the api. These values are calculated from ``onPeakKwh``, ``offPeakKwh``, and the fomula defined by the SRP `TOU price plan sheet <https://srpnet.com/prices/pdfx/April2015/E-26.pdf>`_ 



Installing
==========

It is distributed on PyPI_ and can be installed with pip::

   pip install srpenergy

.. _Srp: https://www.srpnet.com/
.. _PyPI: https://pypi.python.org/pypi/srpenergy

Use
==========

.. code-block:: python

    from datetime import datetime, timedelta
    from srpenergy.client import SrpEnergyClient

    accountid = 'your account id'
    username = 'your username'
    password = 'your password'
    end_date = datetime.now()
    start_date = datetime.now() - timedelta(days=2)

    client = SrpEnergyClient(accountid, username, password)
    usage = client.usage(start_date, end_date)
    
    date, hour, isodate, kwh, cost = usage[0]


Development 
===========



Style Guidelines
----------------

This project enforces quite strict `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ and `PEP257 (Docstring Conventions) <https://www.python.org/dev/peps/pep-0257/>`_ compliance on all code submitted.

We use `Black <https://github.com/psf/black>`_ for uncompromised code formatting.

Summary of the most relevant points:

 - Comments should be full sentences and end with a period.
 - `Imports <https://www.python.org/dev/peps/pep-0008/#imports>`_  should be ordered.
 - Constants and the content of lists and dictionaries should be in alphabetical order.
 - It is advisable to adjust IDE or editor settings to match those requirements.

Ordering of imports
-------------------

Instead of order the imports manually, use `isort <https://github.com/timothycrosley/isort>`_.

.. code-block:: bash

    pip3 install isort
    isort -rc .  


Use new style string formatting
-------------------------------

Prefer `f-strings <https://docs.python.org/3/reference/lexical_analysis.html#f-strings>`_ over ``%`` or ``str.format``.

.. code-block:: python

    #New
    f"{some_value} {some_other_value}"
    # Old, wrong
    "{} {}".format("New", "style")
    "%s %s" % ("Old", "style")

One exception is for logging which uses the percentage formatting. This is to avoid formatting the log message when it is suppressed.

.. code-block:: python

    _LOGGER.info("Can't connect to the webservice %s at %s", string1, string2)

Testing
-------

As it states in the `Style Guidelines`_ section all code is checked to verify the following:

 - All the unit tests pass
 - All code passes the checks from the linting tools

Local testing is done using `Tox <https://tox.readthedocs.io/en/latest/>`_. To start the tests, activate the virtual environment and simply run the command:

.. code-block:: bash

    tox

**Testing outside of Tox**

Running ``tox`` will invoke the full test suite. To be able to run the specific test suites without tox, you'll need to install the test dependencies into your Python environment:

.. code-block:: bash

    pip3 install -r requirements_test.txt

Now that you have all test dependencies installed, you can run tests on the project:

.. code-block:: bash

    isort -rc .
    black srpenergy test
    flake8 srpenergy test
    pylint srpenergy test
    pydocstyle srpenergy test
    python -m pytest test/test_client.py
    python -m pytest --cov-report term-missing --cov=srpenergy

