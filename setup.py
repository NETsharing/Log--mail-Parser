import os
from setuptools import setup, find_packages


setup(
    name='parser',
    version='1.0',
    author='Koblov E V',
    author_email = 'workcenter@mail.ru',
    packages=find_packages(),
    description='Parses mail server logs and provides information about successful shipments.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
)