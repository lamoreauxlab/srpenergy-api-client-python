=========================
Development Documentation
=========================

Build module with::

$ python setup.py bdist_wheel --universal

Publish to pypi test::

$ twine upload --repository-url https://test.pypi.org/srpenergy/ dist/*

Publish to pypi::

$ twine upload dist/*