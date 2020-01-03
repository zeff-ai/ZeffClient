# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff test suite."""
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

import pytest

from zeff.record import (
    Record,
    StructuredData,
    UnstructuredData,
    Target,
    DataType,
    FileType,
)
from zeff.validator import RecordValidator


def test_build():
    """Test building a record.

    This will check to make sure that all dataclasses
    associated with a Record can be built and added to
    appropriate containers.
    """
    r = Record("Test")

    ## StructuredData
    sd = StructuredData("TestName", 1.1, DataType.CONTINUOUS, Target.YES)
    assert sd.record is None
    sd.record = r
    assert sd in list(r.structured_data)
    assert len(list(r.structured_data)) == 1

    ## UnstructuredData
    ud = UnstructuredData("http://example.com", FileType.TEXT)
    assert ud.record is None
    ud.record = r
    assert ud in list(r.unstructured_data)
    assert len(list(r.unstructured_data)) == 1

    ## Validate
    rv = RecordValidator(True)
    rv(r)
