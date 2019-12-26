#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
"""Zeff CLI tool test suite."""
__copyright__ = """Copyright (C) 2019 Ziff, Inc."""
__docformat__ = "reStructuredText en"

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
    oldpath = sys.path

    def reset():
        sys.path = oldpath

    request.addfinalizer(reset)


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
