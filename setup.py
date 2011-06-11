import os
from setuptools import setup, find_packages

cdir = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(cdir, 'readme.rst')).read()
CHANGELOG = open(os.path.join(cdir, 'changelog.rst')).read()

from commonbwc import VERSION

setup(
    name='CommonBWC',
    version=VERSION,
    description="A BlazeWeb component to hold libraries shared by other components and apps.",
    long_description=README + '\n\n' + CHANGELOG,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP'
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
