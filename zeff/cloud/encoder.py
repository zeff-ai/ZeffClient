"""Zeff CLI record encoders."""
__docformat__ = "reStructuredText en"


import json
from zeff.record import (
    Record,
    StructuredData,
    StructuredDataItem,
    UnstructuredData,
    UnstructuredDataItem,
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
            ret["structuredData"] = o.structured_data
            ret["unstructuredData"] = o.unstructured_data
            return ret
        elif isinstance(o, StructuredData):
            return [item for item in o.structured_data_items]
        elif isinstance(o, StructuredDataItem):
            return {
                "name": o.name,
                "value": o.value,
                "dataType": o.data_type.name,
                "target": o.target.name,
            }
        elif isinstance(o, UnstructuredData):
            return [item for item in o.unstructured_data_items]
        elif isinstance(o, UnstructuredDataItem):
            return {
                "data": o.data,
                "fileType": o.file_type.name,
                "groupByName": o.group_by,
            }
        else:
            return super().default(o)