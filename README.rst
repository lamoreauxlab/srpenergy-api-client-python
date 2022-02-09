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

.. note::
    Time of use customers do not receive a ``totalKwh`` or ``totalCost`` from the api. These values are calculated from ``onPeakKwh``, ``offPeakKwh``, and the fomula defined by the SRP `TOU price plan sheet <https://srpnet.com/prices/pdfx/April2015/E-26.pdf>`_

    EZ3 customers show 0.0 for ``totalKwh`` and ``totalCost``. Those values are split between ``onPeak``, ``offPeak``, ``shoulder``, and ``superOffPeak``.

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

For Time of use plans pass in the argument `is_tou`

.. code-block:: python

    from datetime import datetime, timedelta
    from srpenergy.client import SrpEnergyClient

    accountid = 'your account id'
    username = 'your username'
    password = 'your password'
    end_date = datetime.now()
    start_date = datetime.now() - timedelta(days=2)

    client = SrpEnergyClient(accountid, username, password)
    usage = client.usage(start_date, end_date, True)

    date, hour, isodate, kwh, cost = usage[0]


Development
===========

Configure Dev Environment
-------------------------

This section will configure your computer to develop, test, and debug the project.

.. code-block::bash

    # Copy Project to local computer
    cd /path/to/src/
    git clone https://github.com/lamoreauxlab/srpenergy-api-client-python.git
    cd /path/to/src/srpenergy-api-client-python

    # Create Python Virtual Environment and activate
    python -m venv .venv
    source .venv/bin/activate

    # Install Project
    python -m pip install -r requirements_test.txt
    python -m pip install -e .

    # Create git hook scripts
    pre-commit install

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
    isort .


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

Install the test dependencies into your Python environment:

.. code-block:: bash

    pip3 install -r requirements_test.txt

Now that you have all test dependencies installed, you can run tests on the project:

.. code-block:: bash

    isort .
    codespell  --skip="./.*,*.csv,*.json,*.pyc,./docs/_build/*,./htmlcov/*"
    black setup.py srpenergy tests
    flake8 setup.py srpenergy tests
    pylint setup.py srpenergy tests
    pydocstyle setup.py srpenergy tests
    rstcheck README.rst
    python -m pytest tests
    python -m pytest --cov-report term-missing --cov=srpenergy tests

Building Docs
-------------

Build the documentation locally with

.. code-block:: bash

    cd docs
    python -m sphinx -T -b html -d _build/doctrees -D language=en . _build/html

Run Git Pre-commit
------------------

Run pre-commit hooks on the repository.

.. code-block:: bash

    # Run all hooks
    pre-commit run --all-files

    # Run a specific hook
    pre-commit run hook_id


Package and Deploy
------------------

After a successful build, packageing and deploying will:

- Bump Version
- Tag version in git
- Create Release in git
- Release to pypi

Bump Version
^^^^^^^^^^^^

Change the version in the following files:

- srpenergy/__init__.py
- docs/conf.py

Tag Version
^^^^^^^^^^^

Commit, tag, and push the new version

.. code-block:: bash

    git commit -m "Bump version"
    git tag -a 1.3.1 -m "1.3.1"
    git push --tags

Create Release
^^^^^^^^^^^^^^

- Create a new Release
- Name the Release the same as the tag name
- Auto-generate release notes.


Release to pypi
^^^^^^^^^^^^^^^

Upgrade to the latest version of setuptools and create package and test

.. code-block:: bash

    python -m pip install --user --upgrade setuptools wheel # Get latest version
    python setup.py sdist bdist_wheel
    twine check dist/*

Upload the package to test first

.. code-block:: bash

    python -m twine upload --repository testpypi dist/*

Check that package looks ok. After testing, upload to the main repository

.. code-block:: bash

    python -m twine upload dist/*
