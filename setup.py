#!/usr/bin/env python3
"""Srp Energy setup script."""
from datetime import datetime as dt
import os
import sys

from setuptools import find_packages, setup

from srpenergy import __version__ as version

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

PROJECT_PACKAGE_NAME = "srpenergy"
PROJECT_AUTHOR = "Lamoreaux Lab"
PROJECT_COPYRIGHT = " 2018-{}, {}".format(dt.now().year, PROJECT_AUTHOR)
PROJECT_URL = "https://github.com/lamoreauxlab/srpenergy-api-client-python"
PROJECT_EMAIL = "bklamoreaux@gmail.com"

PROJECT_GITHUB_USERNAME = "lamoreauxlab"
PROJECT_GITHUB_REPOSITORY = "srpenergy-api-client-python"

GITHUB_PATH = "{}/{}".format(PROJECT_GITHUB_USERNAME, PROJECT_GITHUB_REPOSITORY)
GITHUB_URL = "https://github.com/{}".format(GITHUB_PATH)

DEV_DOCS_URL = "https://{}.readthedocs.io/".format(PROJECT_GITHUB_REPOSITORY)

PROJECT_URLS = {
    "Bug Reports": "{}/issues".format(GITHUB_URL),
    "Dev Docs": "{}/en/latest/".format(DEV_DOCS_URL),
}

PACKAGES = find_packages(exclude=["tests", "tests.*"])

REQUIRES = ["requests>=2.22.0", "python-dateutil>=2.8.0"]

MIN_PY_VERSION = "3.6"

setup(
    name=PROJECT_PACKAGE_NAME,
    version=version,
    url=PROJECT_URL,
    project_urls=PROJECT_URLS,
    author=PROJECT_AUTHOR,
    author_email=PROJECT_EMAIL,
    packages=PACKAGES,
    install_requires=REQUIRES,
    python_requires=f">={MIN_PY_VERSION}",
    package_data={"srpenergy": ["LICENSE", "README.rst"]},
)
