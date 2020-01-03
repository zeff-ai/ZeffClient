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
__all__ = ["RecordTemporalValidator"]


import typing
import datetime
from .record import RecordValidator
from ..record import UnstructuredData, UnstructuredTemporalData, FileContext


class RecordTemporalValidator(RecordValidator):
    """Zeff Temporal Record Validator.

    This validator will check that required items are in a temporal
    record.

    .. WARNING::
        Only one record whould be validated at a time by a single
        validator object.
    """

    def validate_unstructured_data(self, data: UnstructuredData):
        """Validate a single unstructured data item.

        Subclasses should override this method to validate the data
        property.
        """
        # pylint: disable=no-self-use
        super().validate_unstructured_data(data)
        tdata = typing.cast(UnstructuredTemporalData, data)
        if tdata.temporal_window is None:
            raise ValueError("temporal_window must have a valid time value.")

        sctime = typing.cast(datetime.time, tdata.start_crop_time)
        ectime = typing.cast(datetime.time, tdata.end_crop_time)
        if sctime >= ectime:
            raise ValueError("start_crop_time must be before end_crop_time.")

        for filecontext in tdata.file_contexts:
            self.validate_filecontext(filecontext, 1)

    def validate_filecontext(self, filecontext: FileContext, maxdepth):
        """Validate a file context object.

        :parameter filecontext: The FileContext to validate.

        :parameter maxdepth: Allowed depth of encapsulated subcontexts.
            If this is 0 then subcontexts must be empty. This will
            be decreased on each recursive call of this method.
        """
        if maxdepth <= 0:
            ValueError("Depth of file context exceeds allowed amount.")
        if filecontext.start_time >= filecontext.end_time:
            ValueError("FileContext start_time must be before end_time.")
        for subcontext in filecontext.subcontexts:
            self.validate_filecontext(subcontext, (maxdepth - 1))
