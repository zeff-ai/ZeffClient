# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff structured data."""
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
# pylint: disable=duplicate-code
# pylint: disable=too-few-public-methods
__all__ = ["StructuredData"]

import dataclasses
from .symbolic import Target, DataType


@dataclasses.dataclass(eq=True)
class StructuredData:
    """Single item of structured data in a record.

    A structured data is a mapping of ``name`` to ``value`` with
    additional information about the ``value``.

    :property name: The unique key that identifies this data item.

    :property value: The value stored in this data item.

    :property target: How a data item is to be used in training or inference.
        This  property is ignored by temporal records (`TemporalRecord`),
        and will not be sent to the Cloud API.

    :property data_type: Is the data continuous or discrete.

    :property record: The record for this data item. Setting this
        property will add this item to ``Record.structured_data``
        list automatically.
    """

    name: str
    value: object
    data_type: DataType
    target: Target = Target.IGNORE

    __record: object = None

    @property
    def record(self):
        """Record that contains this structured data item."""
        return self.__record

    @record.setter
    def record(self, value):
        del self.record
        self.__record = value
        value.structured_data.append(self)

    @record.deleter
    def record(self):
        if self.__record:
            self.__record.structured_data.remove(self)
            self.__record = None
