#!/usr/bin/env python3
"""Srp Energy setup script."""
import os
import sys
from datetime import datetime as dt
from srpenergy import __version__ as version
from setuptools import setup, find_packages

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    sys.exit()

PROJECT_NAME = 'Srp Energy'
PROJECT_PACKAGE_NAME = 'srpenergy'
PROJECT_LICENSE = 'MIT'
PROJECT_AUTHOR = 'Lamoreaux Lab'
PROJECT_COPYRIGHT = ' 2018-{}, {}'.format(dt.now().year, PROJECT_AUTHOR)
PROJECT_URL = 'https://github.com/lamoreauxlab/srpenergy-api-client-python'
PROJECT_EMAIL = 'bklamoreaux@gmail.com'

PROJECT_GITHUB_USERNAME = 'lamoreauxlab'
PROJECT_GITHUB_REPOSITORY = 'srpenergy-api-client-python'

GITHUB_PATH = '{}/{}'.format(
    PROJECT_GITHUB_USERNAME, PROJECT_GITHUB_REPOSITORY)
GITHUB_URL = 'https://github.com/{}'.format(GITHUB_PATH)

DEV_DOCS_URL = 'https://{}.readthedocs.io/'.format(PROJECT_GITHUB_REPOSITORY)

PROJECT_URLS = {
    'Bug Reports': '{}/issues'.format(GITHUB_URL),
    'Dev Docs': '{}/en/latest/'.format(DEV_DOCS_URL),
}

PACKAGES = find_packages(exclude=['tests', 'tests.*'])

REQUIRES = [
    'requests>=1.6',
    'beautifulsoup4>=4.5',
]

MIN_PY_VERSION = '3.5.3'


def read(fname):
    """Read README.rst into long_description.

    ``long_description`` is what ends up on the PyPI front page.
    """
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        contents = f.read()

    return contents


setup(
    name=PROJECT_PACKAGE_NAME,
    version=version,
    url=PROJECT_URL,
    project_urls=PROJECT_URLS,
    author=PROJECT_AUTHOR,
    author_email=PROJECT_EMAIL,
    packages=PACKAGES,
    install_requires=REQUIRES,
    python_requires='>={}'.format(MIN_PY_VERSION),
    description=(
        "An unofficial Python module for interacting with Srp Energy data"),
    long_description=read('README.rst'),
    license='MIT',
    keywords="energy API wrapper srp",
    package_data={
        'srpenergy': [
            'LICENSE', 'README.rst'
        ]
    },
)
