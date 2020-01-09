# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff record."""
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
# pylint: disable=too-few-public-methods
__all__ = ["Record"]

import dataclasses
import typing
from .structureddata import StructuredData
from .unstructureddata import UnstructuredData


@dataclasses.dataclass()
class Record:
    """This represents a single record in Zeff.

    :property name: The unique name for the record.

    :property structured_data: List of ``StructuredData`` objects that
        belong to this record. This list should not be modified directly;
        setting ``StructuredData.record`` property will add the object
        to the list.

    :property unstructured_data: List of ``UnstructuredData`` objects that
        belong to this record. This list should not be modified directly;
        setting ``UnstructuredData.record`` property will add the object
        to the list.
    """

    name: str
    structured_data: typing.List[StructuredData] = dataclasses.field(
        default_factory=list
    )
    unstructured_data: typing.List[UnstructuredData] = dataclasses.field(
        default_factory=list
    )

    def __str__(self):
        """`__str__<https://docs.python.org/3/reference/datamodel.html#object.__str__>`_."""
        return self.name
