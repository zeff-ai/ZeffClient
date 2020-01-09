# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff unstructured data."""
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
__all__ = ["UnstructuredData"]

import dataclasses
from typing import Optional
from .symbolic import FileType


@dataclasses.dataclass(eq=True)
class UnstructuredData:
    """Single item of unstructured data in a record.

    An unstructured data is a URI to ``data`` that has an
    associated file type and may be grouped with other similar
    data.

    :property data_uri: URI to the raw data.

    :property file_type: The file type of the data.

    :property group_by: Name of group this item should be
        associated with.

    :property upload: Indicates that the ``data`` should be uploaded
        to the Zeff API when this data item is uploaded (default is
        for the server to access the data directly using the URL in
        ``data``).

    :property accessible: Flag set during validation that the
        location given by ``data_uri`` is accessible.

    :property record: The record for this data item. Setting this
        property will add this item to ``Record.unstructured_data``
        list automatically.
    """

    data_uri: str
    file_type: FileType
    group_by: Optional[str] = None
    upload: bool = False
    accessible: str = dataclasses.field(
        default="", init=False, repr=False, compare=False
    )
    __record: object = None

    @property
    def record(self):
        """Record that contains this unstructured data item."""
        return self.__record

    @record.setter
    def record(self, value):
        del self.record
        self.__record = value
        value.unstructured_data.append(self)

    @record.deleter
    def record(self):
        if self.__record:
            self.__record.unstructured_data.remove(self)
            self.__record = None
