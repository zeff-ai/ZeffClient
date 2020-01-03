#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff CLI tool test suite."""
__author__ = """Lance Finn Helsten <lanhel@zeff.ai>"""
__copyright__ = """Copyright © 2019, Ziff, Inc. — All Rights Reserved"""
__license__ = """
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import sys
import os
import pathlib
import pytest


@pytest.fixture(scope="function")
def chdir(request):
    """Reset CWD directory:

        1. At start of test the CWD will be in the directory that
           contains the test file.

        2. After test completes the CWD will be reset to the CWD
           before the test started.
    """
    oldcwd = pathlib.Path.cwd()
    request.fspath.dirpath().chdir()

    def reset():
        os.chdir(oldcwd)

    request.addfinalizer(reset)


@pytest.fixture(scope="function")
def sys_path(request):
    """Reset sys.path."""
    oldpath = list(sys.path)

    def reset():
        sys.path = oldpath

    request.addfinalizer(reset)


@pytest.fixture(scope="function")
def test_path(request, sys_path):
    """Add the directory that contains the test to sys.path."""
    path = os.path.dirname(request.module.__file__)
    sys.path.append(path)


def OFF_load_tests(loader, tests, pattern):
    import importlib

    for name in [".test_compile"]:
        m = importlib.import_module(name, __package__)
        m_tests = loader.loadTestsFromModule(m, pattern)
        tests.addTests(m_tests)
    return tests


def OFF_test_suite():
    """Used by setuptools test command to load the suite."""
    import unittest

    loader = unittest.TestLoader()
    return loader.loadTestsFromModule(__package__)
