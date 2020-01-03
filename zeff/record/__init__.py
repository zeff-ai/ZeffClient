# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""ZeffClient Record.

A record is a collection of information that will be used to train
a machine, or on which the machine may make an inferance. The information
is contained in sets of strutured and unstructured data.

Structured data is dictionary of key-value items where the value has
either a continuous type (e.g. integer or floating point) or a discrete
type. This data may be marked to use for training, for inference, or
to be ignored by the machine.

Unstructured data is a stream of data that has media-type (e.g.
image/jpeg or video/mpeg) and an optional tag that will group it with
other unstructured data.

.. uml:: uml/recordClassDiagram.uml
   :scale: 50 %
   :align: center
"""
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
__all__ = [
    "Record",
    "StructuredData",
    "UnstructuredData",
    "UnstructuredTemporalData",
    "Target",
    "DataType",
    "FileType",
]

from .symbolic import *
from .record import *
from .structureddata import *
from .unstructureddata import *
from .unstructuredtemporaldata import *
from .file import *
from .formatter import *
