#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ----------------------------------------------------------------------------
"""ZeffClient is a collection of libraries and tools to simplify working
with Zeff Cloud API."""
__copyright__ = """Copyright (C) 2019 Ziff, Inc."""
__author__ = ('Lance Finn Helsten', )
__version__ = '0.0.0'

import sys
import os

from setuptools import setup, find_packages
setup(
    name='ZeffClient',
    version=__version__,
    author='Lance Finn Helsten',
    author_email='lanhel@flyingtitans.com',
    maintainer='Lance Finn Helsten',
    maintainer_email='lanhel@flyingtitans.com',
    url='https://github.com/zeffai/zeffclient',
    description=__doc__,
    long_description=open('README.rst').read(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Data Science",
        "License :: Other/Proprietary License",
        "Operating System :: POSIX",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">= 3.7",
    setup_requires=[
        "docutils >= 0.14",
    ],
    install_requires=[
        "PyYAML >= 3.11",
        "pyaml >= 15.0",
    ],
    extras_require={
        'docs': [
            "docutils>=0.3",
        ],
        'tests': [
            "coverage>=4.0",
            "hypothesis>=4.23",
        ],
        'dev': [
            "coverage>=4.0",
            "hypothesis>=4.23",
            "docutils>=0.3"
        ]
    },
    packages=[
        'zeff',
        'zefflib'
    ],
    package_data={
        'zeff': [
            '*.txt'
        ],
        'zefflib': [
        ]
    },
    entry_points={
        'console_scripts': [
            'zeff = zeff.__main__:main'
        ]
    },
    test_suite="tests.zefflibTestSuite",
    data_files=[],
)
