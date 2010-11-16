"""
Introduction
---------------

CommonBWC is a component for `BlazeWeb <http://pypi.python.org/pypi/BlazeWeb/>`_
applications.  It has views, classes, and templates that are common for many
web applications.

Questions & Comments
---------------------

Please visit: http://groups.google.com/group/blazelibs

Current Status
---------------

The code stays pretty stable, but the API is likely to change in the future.

The `CommonBWC tip <http://bitbucket.org/rsyring/commonbwc/get/tip.zip#egg=commonbwc-dev>`_
is installable via `easy_install` with ``easy_install commonbwc==dev``
"""

from setuptools import setup, find_packages

from commonbwc import VERSION

setup(
    name='CommonBWC',
    version=VERSION,
    description="A BlazeWeb component to hold libraries shared by other components and apps.",
    long_description = __doc__,
    classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    ],
    author='Randy Syring',
    author_email='rsyring@gmail.com',
    url='http://bitbucket.org/rsyring/commonbwc/',
    license='BSD',
    packages=find_packages(exclude=['commonbwc_*']),
    include_package_data = True,
    zip_safe=False,
    install_requires=[
        'BlazeForm>=0.3.0',
        'BlazeWeb>=0.3.0',
    ],
)
