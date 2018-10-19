import os
import sys
from srpenergy import __version__ as version

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    sys.exit()


def read(fname):
    """Utility function to get README.rst into long_description.
    ``long_description`` is what ends up on the PyPI front page.
    """
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        contents = f.read()

    return contents


setup(
    name='srpenergy',
    version=version,
    author="Lamoreaux Lab",
    author_email='bklamoreaux@gmail.com',
    description=(
        "An unofficial Python module for interacting with Srp Energy data"),
    long_description=read('README.rst'),
    license='MIT',
    keywords="energy API wrapper srp",
    url='https://github.com/lamoreauxlab/srpenergy-api-client-python',
    packages=['srpenergy'],
    package_data={'srpenergy': ['LICENSE', 'README.rst']},
    install_requires=['requests>=1.6'],
)
