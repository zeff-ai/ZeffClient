# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff unstructured temporal data."""
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
__all__ = ["UnstructuredTemporalData"]

import dataclasses
import typing
import datetime
from .file import FileContext
from .unstructureddata import UnstructuredData


@dataclasses.dataclass
class UnstructuredTemporalData(UnstructuredData):
    """Single item of unstructured temporal data in a record.

    :property temporal_window: Size of window to analyze. This
        is a required property and if missing the data will
        fail in validation.

    :property start_crop_time: Time location from begining of file
        that will mark the start of the interval. Content before start
        point will not be used to train the Ai.

    :property end_crop_time: Time location from begining of file
        that will mark the end of the interval. Content after end
        point will not be used to train the Ai.

    :property file_context:
    """

    temporal_window: typing.Optional[datetime.time] = None
    start_crop_time: typing.Optional[datetime.time] = None
    end_crop_time: typing.Optional[datetime.time] = None
    file_contexts: typing.List[FileContext] = dataclasses.field(default_factory=list)
