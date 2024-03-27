**********************************
Srp Energy Developer APIs - Python
**********************************
.. image:: https://coveralls.io/repos/github/lamoreauxlab/srpenergy-api-client-python/badge.svg?branch=main
    :target: https://coveralls.io/github/lamoreauxlab/srpenergy-api-client-python?branch=main
    :alt: Coverage Status

.. image:: https://readthedocs.org/projects/srpenergy-api-client-python/badge/?version=latest
    :target: https://srpenergy-api-client-python.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

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
    Time of use customers do not receive a ``totalKwh`` or ``totalCost`` from the api. These values are calculated from ``onPeakKwh``, ``offPeakKwh``, and the formula defined by the SRP `TOU price plan sheet <https://srpnet.com/prices/pdfx/April2015/E-26.pdf>`_

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

You'll need to set up a development environment if you want to develop a new feature or fix issues. The project uses a docker based devcontainer to ensure a consistent development environment.
- Open the project in VSCode and it will prompt you to open the project in a devcontainer. This will have all the required tools installed and configured.

Setup local dev environment
---------------------------

If you want to develop outside of a docker devcontainer you can use the following commands to setup your environment.

* Install Python
* Configure linting and formatting tools

.. code-block:: bash

    # Clone Project to local computer
    cd /path/to/src/
    git clone https://github.com/lamoreauxlab/srpenergy-api-client-python.git
    cd srpenergy-api-client-python

    # Configure the environment variables. Copy example.env to .env and update the values
    cp example.env .env

    # load .env vars
    # [ ! -f .env ] || export $(grep -v '^#' .env | xargs)
    # or this version allows variable substitution and quoted long values
    # [ -f .env ] && while IFS= read -r line; do [[ $line =~ ^[^#]*= ]] && eval "export $line"; done < .env

    # Linux
    # virtualenv .venv /usr/local/bin/python3.10
    python3 -m venv .venv
    source .venv/bin/activate

    # Windows
    # virtualenv \path\to\.venv -p path\to\specific_version_python.exe
    # C:\Users\!Admin\AppData\Local\Programs\Python\Python310\python.exe -m venv .venv
    # .venv\scripts\activate

    # Update pip
    python -m pip install --upgrade pip

    # Install dependencies
    python -m pip install -r requirements_dev.txt

    # Configure linting and formatting tools
    sudo apt-get update
    sudo apt-get install -y shellcheck
    pre-commit install

    # Install the package locally
    pip install --editable .

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

.. code-block:: bash

    # Use pre-commit scripts to run all linting
    pre-commit run --all-files

    # Run a specific linter via pre-commit
    pre-commit run --all-files codespell

    # Run linters outside of pre-commit
    codespell .
    shellcheck -x ./script/*.sh
    rstcheck README.rst

    # Run unit tests
    python -m pytest tests
    python -m pytest --cov-report=xml --cov-report term-missing --cov=srpenergy tests/

Building Docs
-------------

Build the documentation locally with

.. code-block:: bash

    cd docs
    sphinx-build -T -b html -d _build/doctrees -D language=en . _build/html

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

    python -m pip install --upgrade build twine
    python -m build
    twine check dist/*

Upload the package to test first

.. code-block:: bash

    python -m twine upload --repository testpypi dist/*

Check that package looks ok. After testing, upload to the main repository

.. code-block:: bash

    python -m twine upload dist/*
