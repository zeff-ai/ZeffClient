"""Zeff CLI test suite."""

import sys
import os
import io
import types

from zeff.cli.__main__ import main


def OFF_test_help():
    # This will cause the entire system to exit
    main(args=["--help"])
