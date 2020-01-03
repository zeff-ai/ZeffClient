# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff Validator."""
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
__all__ = ["RecordGeospatialValidator"]


import typing
from .generic import RecordGenericValidator


class RecordGeospatialValidator(RecordGenericValidator):
    """Zeff Geospatial Record Validator.

    This validator will check that required items are in a geospatial
    record.

    .. WARNING::
        Only one record whould be validated at a time by a single
        validator object.
    """

    def validate_structured_data_aggregation(self, names: typing.Iterable[str]):
        """Check that `latitude` and `longitude` are available."""
        if "latitude" not in names:
            raise ValueError("Missing latitude data item.")
        if "longitude" not in names:
            raise ValueError("Missing longitude data item.")
