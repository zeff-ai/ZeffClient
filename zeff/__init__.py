# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff client library to Zeff Cloud API.

Zeff is a Python package that dimplifies the creation, modification,
and uploading of records to Zeff Cloud API.


Environment
===========


Loggers
=======

- ``zeffclient.record.builder``
    Logger that should be used by record builder's, including those
    made by users of ZeffClient.

- ``zeffclient.record.generator``
    Logger used by the record generation subsystem.

- ``zeffclient.record.validator``
    Logger used by the record validation subsystem.

- ``zeffclient.record.uploader``
    Logger used by the record upload subsystem.

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

import pkg_resources

try:
    __version__ = pkg_resources.get_distribution("ZeffClient").version
except pkg_resources.DistributionNotFound as err:
    __version__ = "0.0.0"


from .pipeline import Counter, record_builder_generator, validation_generator
from .pipeline_observation import *

# pylint: disable=duplicate-code

from .uploader import Uploader
from .predictor import Predictor
