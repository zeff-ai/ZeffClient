# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff record file reference."""
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
__all__ = ["FileContext"]

import dataclasses
import typing
import datetime
from .symbolic import DataType


@dataclasses.dataclass(eq=True, frozen=True)
class FileContext:
    """Structured data associated with a time interval.

    .. caution:: Subcontext is only allowed to be used in a
        FileContext that is added directly to an unstructured
        temporal data object.
    """

    name: str
    value: object
    data_type: DataType
    start_time: datetime.time
    end_time: datetime.time
    subcontexts: typing.List["FileContext"] = dataclasses.field(default_factory=list)
