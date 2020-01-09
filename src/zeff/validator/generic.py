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
__all__ = ["RecordGenericValidator"]

from .record import RecordValidator
from ..record import Record, StructuredData, UnstructuredData, Target


class RecordGenericValidator(RecordValidator):
    """Zeff Generic Record Validator.

    See RecordValidator.
    """

    def __init__(self, *argv, **kwargs):
        """See RecordValidator.__init__."""
        super().__init__(*argv, **kwargs)
        self.has_target = False

    def reset(self):
        """See RecordValidator.reset."""
        self.has_target = False

    def validate_record(self, record: Record):
        """See RecordValidator.validate_record."""
        if self.model:
            pass
        else:
            if len(record.structured_data) < 1:
                raise ValueError(
                    "Dataset record must have at least one StructuredData item."
                )
            if not self.has_target:
                raise ValueError(
                    "Record for dataset must have a target StructuredData item."
                )

    def validate_structured_data(self, data: StructuredData):
        """See RecordValidator.validate_structured_data."""
        super().validate_structured_data(data)
        if data.target == Target.YES:
            self.has_target = True

    def validate_unstructured_data(self, data: UnstructuredData):
        """See RecordValidator.validate_unstructured_data."""
        # pylint: disable=unidiomatic-typecheck
        super().validate_unstructured_data(data)
        if type(data) != UnstructuredData:
            raise ValueError("Subclass of UnstructuredData not allowed.")
