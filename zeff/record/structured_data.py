"""Zeff structured data."""
# pylint: disable=duplicate-code
# pylint: disable=too-few-public-methods
__docformat__ = "reStructuredText en"

import dataclasses

from .record import Record
from .aggregator import aggregation


@aggregation(Record)
@dataclasses.dataclass(unsafe_hash=True)
class StructuredData():
    """This represents a set of structured data items."""


@aggregation(StructuredData)
@dataclasses.dataclass(eq=True, frozen=True)
class StructuredDataItem():
    """Single item in StruturedData.

    A structured data item is a mapping of ``name`` to ``value``
    with additional information about the ``value``.

    :property name: The unique key that identifies this item.

    :property value: The value stored in this item.

    :property target: TBW

    :property data_type: Is the data continuous or discrete.
    """

    name: str
    value: str
    target: str
    data_type: str
