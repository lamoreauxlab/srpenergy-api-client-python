*******************
Lamoreaux Lab Srp Energy Developer APIs - Python
*******************
.. image:: https://travis-ci.org/lamoreauxlab/srpenergy-api-client-python.svg?branch=master
    :target: https://travis-ci.org/lamoreauxlab/srpenergy-api-client-python

.. image:: https://coveralls.io/repos/github/lamoreauxlab/srpenergy-api-client-python/badge.svg?branch=master
    :target: https://coveralls.io/github/lamoreauxlab/srpenergy-api-client-python?branch=master

.. image:: https://readthedocs.org/projects/srpenergy-api-client-python/badge/?version=latest
    :target: https://srpenergy-api-client-python.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

An unofficial Python module for interacting with Srp Energy data.

Use
############

.. code-block:: python

    from srpenergy.client import SrpEnergyClient

    username = 'your username'
    password = 'your password'
    client = SrpEnergyClient(username, password)
    usage = client.usage(start_date, end_date)
