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
import enum

from zeff.record import StructuredData, Target, DataType
from zeff.validator import RecordValidator


def test_build():
    """Test building a StructuredData."""
    validator = RecordValidator(True)

    sd0 = StructuredData("TestName", 1.1, DataType.CONTINUOUS, Target.YES)
    assert sd0.record is None
    validator.validate_structured_data(sd0)

    sd1 = StructuredData("TestName", "TestValue", DataType.CATEGORY, Target.YES)
    assert sd1.record is None
    validator.validate_structured_data(sd1)


def test_invalid_strutureddatatype():
    """Attempt to add an invalid data type to a StructuredData."""
    validator = RecordValidator(True)

    with pytest.raises(TypeError):
        sd = StructuredData("TestName", "TestValue", DataType.CONTINUOUS, "TestTarget")
        validator.validate_structured_data(sd)
    with pytest.raises(TypeError):
        sd = StructuredData("TestName", "TestValue", "TestDataType", Target.YES)
        validator.validate_structured_data(sd)


def test_invalid_structuredtarget():
    """TBW"""
    validator = RecordValidator(True)
    with pytest.raises(ValueError):
        sd = StructuredData("TestName", "abc", DataType.CONTINUOUS, Target.NO)
        validator.validate_structured_data(sd)


@pytest.mark.skip()
def test_unknown_structureddatatype():
    """Check to make sure a test will fail if a new data type is added."""
    global DataType

    class TestDataType(enum.Enum):
        CONTINUOUS = enum.auto()
        CATEGORY = enum.auto()
        SPAM = enum.auto()

    validator = RecordValidator(True)
    old = DataType
    with pytest.raises(ValueError):
        DataType = TestDataType
        sd = StructuredData("TestName", "abc", DataType.SPAM, Target.NO)
        validator.validate_structured_data(sd)
    DataType = old
