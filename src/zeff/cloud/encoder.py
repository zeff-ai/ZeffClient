# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff CLI record encoders."""
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


import json
from zeff.record import (
    Record,
    StructuredData,
    UnstructuredData,
    UnstructuredTemporalData,
    FileContext,
)


class RecordEncoder(json.JSONEncoder):
    """Encode Zeff Records."""

    # pylint: disable=method-hidden

    def default(self, o):
        """Return primative objects for Record."""
        # pylint: disable=no-else-return
        if isinstance(o, Record):
            ret = {}
            ret["name"] = {
                "uniqueName": str(o.name),
                "sortAscending": True,
                "holdoutRecord": True,
            }
            if len(o.structured_data) > 0:
                ret["structuredData"] = o.structured_data
            if len(o.unstructured_data) > 0:
                ret["unstructuredData"] = o.unstructured_data
            return ret
        elif isinstance(o, StructuredData):
            return {
                "name": o.name,
                "value": o.value,
                "dataType": o.data_type.name,
                "target": o.target.name,
            }
        elif isinstance(o, UnstructuredTemporalData):
            raise NotImplementedError()
            # return {
            #     "data": o.data_uri,
            #     "fileType": o.file_type.name,
            #     "groupByName": o.group_by,
            # }
        elif isinstance(o, UnstructuredData):
            return {
                "data": o.data_uri,
                "fileType": o.file_type.name,
                "groupByName": o.group_by,
            }
        elif isinstance(o, FileContext):
            raise NotImplementedError()
        else:
            return super().default(o)
