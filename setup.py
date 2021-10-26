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
PROJECT_COPYRIGHT = f" 2018-{dt.now().year}, {PROJECT_AUTHOR}"
PROJECT_URL = "https://github.com/lamoreauxlab/srpenergy-api-client-python"
PROJECT_EMAIL = "bklamoreaux@gmail.com"

PROJECT_GITHUB_USERNAME = "lamoreauxlab"
PROJECT_GITHUB_REPOSITORY = "srpenergy-api-client-python"

GITHUB_PATH = f"{PROJECT_GITHUB_USERNAME}/{PROJECT_GITHUB_REPOSITORY}"
GITHUB_URL = f"https://github.com/{GITHUB_PATH}"

DEV_DOCS_URL = f"https://{PROJECT_GITHUB_REPOSITORY}.readthedocs.io/"

PROJECT_URLS = {
    "Bug Reports": f"{GITHUB_URL}/issues",
    "Dev Docs": f"{DEV_DOCS_URL}/en/latest/",
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
