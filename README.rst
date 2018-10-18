*******************
Lamoreaux Lab Srp Energy Developer APIs - Python
*******************
.. image:: https://travis-ci.org/lamoreauxlab/srpenergy-api-client-python.svg?branch=master
    :target: https://travis-ci.org/lamoreauxlab/srpenergy-api-client-python
    
An unofficial Python module for interacting with Srp Energy data.

Use
############

.. code-block:: python

    from srpenergy.client import SrpEnergyClient

    username = 'your username'
    password = 'your password'
    client = SrpEnergyClient(username, password)
    usage = client.usage(start_date, end_date)
