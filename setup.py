import os
from setuptools import setup, find_packages

cdir = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(cdir, 'readme.rst')).read()
CHANGELOG = open(os.path.join(cdir, 'changelog.rst')).read()
VERSION = open(os.path.join(cdir, 'commonbwc', 'version.txt')).read().strip()

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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP'
    ],
    author='Randy Syring',
    author_email='randy.syring@level12.io',
    url='https://github.com/blazelibs/commonbwc/',
    license='BSD',
    packages=find_packages(exclude=['commonbwc_*']),
    include_package_data = True,
    zip_safe=False,
    install_requires=[
        'BlazeForm>=0.3.0',
        'BlazeWeb>=0.3.0',
    ],
    extras_require={
        'dev': [
            'codecov',
            'coverage',
            'flake8',
            'nose',
            'pyquery',
            'tox',
            'webtest',
            'wheel',
        ]
    }
)
