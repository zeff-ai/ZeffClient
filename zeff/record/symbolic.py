# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff record symbols."""
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
__all__ = ["Target", "DataType", "FileType"]

import enum


class Target(enum.Enum):
    """How the data item is to be used in training or inference.

    - YES
        This is a desired outcome to be predicted.

    - NO
        This is an input to consume for predictions.

    - IGNORE
        Do not use in training or predition but may show in reporting
    """

    YES = enum.auto()
    NO = enum.auto()
    IGNORE = enum.auto()


class DataType(enum.Enum):
    """Data type of a structured data item.

    - CONTINUOUS
        Continuous data type such as integer or floating point.

    - CATEGORY
        Discrete data type such as a string.
    """

    CONTINUOUS = enum.auto()
    CATEGORY = enum.auto()


class FileType(enum.Enum):
    """File type of a unstructured data item."""

    IMAGE = enum.auto()
    AUDIO = enum.auto()
    VIDEO = enum.auto()
    DOCUMENT = enum.auto()
    META = enum.auto()
    TEXT = enum.auto()
