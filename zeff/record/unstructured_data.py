"""Zeff unstructured data."""
# pylint: disable=duplicate-code
# pylint: disable=too-few-public-methods
__docformat__ = "reStructuredText en"

import dataclasses
from typing import Optional

from .aggregator import aggregation
from .record import Record


@aggregation(Record)
@dataclasses.dataclass(unsafe_hash=True)
class UnstructuredData:
    """This represents a set of unstructured data items."""

    def validate(self):
        """Validate to ensure that it will be accepted on upload."""
        # pylint: disable=no-member
        for item in self.structured_data_items:
            item.validate()


@aggregation(UnstructuredData, contained_prop_name="unstructured_data_items")
@dataclasses.dataclass(eq=True, frozen=True)
class UnstructuredDataItem:
    """Single item in UnstruturedData.

    An unstructured data time is a URI to ``data`` that has an
    associated media type and may be grouped with other similar
    data.

    :property data: URI to the raw data.

    :property media_type: An RFC 2046 media type of the data.

    :property group_by: Name of a groupd this item should be
    associated with.
    """

    data: str
    media_type: str
    group_by: Optional[str] = None

    def validate(self):
        """Validate to ensure that it will be accepted on upload."""
        pass
