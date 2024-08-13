from setuptools import setup, find_packages

setup(
    name='rldiff',
    version='0.0.1',
    packages=find_packages(
        where='.',
        include=['*']
    ),
)