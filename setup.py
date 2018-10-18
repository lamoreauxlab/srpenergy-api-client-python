import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="srpenergy",
    version="1.0dev",
    author="Lamoreaux Lab",
    author_email="bklamoreaux@gmail.com",
    description=(
        "An unofficial Python module for interacting with Srp Energy data"),
    license="MIT",
    keywords="energy API wrapper srp",
    url="https://github.com/lamoreauxlab/srpenergy-api-client-python",
    packages=['srpenergy'],
    package_data={'srpenergy': ['LICENSE', 'README.rst']},
    long_description=open('README.rst').read(),
    install_requires=['requests>=1.6'],
)