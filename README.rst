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

Srp provides an hourly energy usage report for their customers. The ``srpenergy`` module fetches the data found on the website.

+-----------+----------+-----+-------+ 
|Usage Date | Hour     | kWh | Cost  |
+===========+==========+=====+=======+
|9/19/2018  | 12:00 AM | 1.2 | $0.17 |
+-----------+----------+-----+-------+
|9/19/2018  | 1:00 AM  | 2.1 | $0.30 |
+-----------+----------+-----+-------+
|9/19/2018  | 2:00 AM  | 1.5 | $0.23 |
+-----------+----------+-----+-------+
|9/19/2018  | 3:00 AM  | 1.3 | $0.20 |
+-----------+----------+-----+-------+
|9/19/2018  | 4:00 AM  | 1.5 | $0.23 | 
+-----------+----------+-----+-------+
|9/19/2018  | 5:00 AM  | 1.5 | $0.23 |
+-----------+----------+-----+-------+


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
