# -*- coding: utf-8 -*-
from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

setup(
    name='''evaluation''',

    # Author details
    author='''Florian Woerister''',
    author_email='''e1126205@student.tuwien.ac.at''',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*', 'ckanext']),
    namespace_packages=['evaluation']
)
