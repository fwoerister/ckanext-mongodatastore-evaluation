# -*- coding: utf-8 -*-
from setuptools import setup, find_packages  # Always prefer setuptools over distutils

setup(
    name='''ckanext-mongodatastore-evaluation''',

    # Author details
    author='''Florian Woerister''',
    author_email='''e1126205@student.tuwien.ac.at''',

    packages=find_packages(),
    namespace_packages=['evaluation'],

    license='GNU Affero General Public License v3 or later (AGPLv3+)',
    classifiers=[
        # How mature is this project? Common values are
        # 3 - Alpha
        # 4 - Beta
        # 5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.8',
    ],
)
