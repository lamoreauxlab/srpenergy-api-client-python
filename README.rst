*******************
Lamoreaux Lab Srp Energy Developer APIs - Python
*******************
An unofficial Python module for interacting with Srp Energy data.

Use
############

.. code-block:: python

    from srpenergy.client import SrpEnergyClient

    username = 'your username'
    password = 'your password'
    client = SrpEnergyClient(username, password)
    usage = client.get_usage(start_date, end_date)
