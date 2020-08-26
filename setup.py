# -*- coding: utf-8 -*-
from setuptools import setup, find_packages  # Always prefer setuptools over distutils

setup(
    name='''ckanext-mongodatastore-evaluation''',

    # Author details
    author='''Florian Woerister''',
    author_email='''e1126205@student.tuwien.ac.at''',

    packages=find_packages(),
    namespace_packages=['evaluation']
)
