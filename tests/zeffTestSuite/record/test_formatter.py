# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff test formatters."""
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
from io import StringIO
from zeff.record import (
    Record,
    StructuredData,
    UnstructuredData,
    Target,
    DataType,
    format_record_restructuredtext,
)


def test_format_record_restructuredtext():
    """TBW."""
    r = Record("Formatted Record")

    sd_info = [
        ("sold_price", 1368411.0, DataType.CONTINUOUS, Target.NO),
        ("basement", 2412.0, DataType.CONTINUOUS, Target.NO),
        (
            "garage_parking",
            "uncovered; rv parking; storage above; extra length; workbench",
            DataType.CATEGORY,
            Target.NO,
        ),
        ("lot", "auto-part; private", DataType.CATEGORY, Target.NO),
    ]
    for info in sd_info:
        sd = StructuredData(*info)
        sd.record = r

    ud_info = [
        ("https://www.example.com/properties/photo_5.jpg", "image/jpg", "home_photo"),
        ("https://www.example.com/properties/photo_37.jpg", "image/jpg", "home_photo"),
        ("https://www.example.com/properties/photo_6.jpg", "image/jpg", "home_photo"),
    ]
    for info in ud_info:
        ud = UnstructuredData(*info)
        ud.record = r

    result = StringIO()
    format_record_restructuredtext(r, out=result)
