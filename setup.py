from setuptools import setup, find_packages

from commonbwp import VERSION

setup(
    name='CommonBWP',
    version=VERSION,
    description="A BlazeWeb component to hold libraries shared by other components and apps.",
    classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    ],
    author='Randy Syring',
    author_email='rsyring@gmail.com',
    url='',
    license='BSD',
    packages=find_packages(exclude=['cbwptestapp']),
    zip_safe=False,
    install_requires=[
        'BlazeForm>=0.3.0dev',
        'BlazeWeb>=0.3.0dev',
    ],
)
