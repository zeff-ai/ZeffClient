#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
"""Zeff recordgenerator test suite."""
__copyright__ = """Copyright (C) 2019 Ziff, Inc."""
__docformat__ = "reStructuredText en"


def OFF_load_tests(loader, tests, pattern):
    import importlib
    for name in [
            ".test_reporter"
        ]:
        m = importlib.import_module(name, __package__)
        m_tests = loader.loadTestsFromModule(m, pattern)
        tests.addTests(m_tests)
    return tests


def OFF_test_suite():
    """Used by setuptools test command to load the suite."""
    import unittest
    loader = unittest.TestLoader()
    return loader.loadTestsFromModule(__package__)

