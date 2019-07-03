"""Zeff structured data."""
# pylint: disable=duplicate-code
# pylint: disable=too-few-public-methods
__docformat__ = "reStructuredText en"

import dataclasses
import enum

from .record import Record
from .aggregator import aggregation


@aggregation(Record)
@dataclasses.dataclass(unsafe_hash=True)
class StructuredData:
    """This represents a set of structured data items."""

    def validate(self):
        """Validate to ensure that it will be accepted on upload."""
        # pylint: disable=no-member
        for item in self.structured_data_items:
            item.validate()


@aggregation(StructuredData, contained_prop_name="structured_data_items")
@dataclasses.dataclass(eq=True, frozen=True)
class StructuredDataItem:
    """Single item in StruturedData.

    A structured data item is a mapping of ``name`` to ``value``
    with additional information about the ``value``.

    :property name: The unique key that identifies this item.

    :property value: The value stored in this item.

    :property target: How a data item is to be used in training or inference.
        - YES is a desired outcome to be predicted
        - NO is an input to consume for prediction
        - IGNORE do not use in training or predition but may show in reporting

    :property data_type: Is the data continuous or discrete.
    """

    class Target(enum.Enum):
        """How the data item is to be used in training or inference."""

        YES = enum.auto()
        NO = enum.auto()
        IGNORE = enum.auto()

    class DataType(enum.Enum):
        """Data type of a structured data item."""

        CONTINUOUS = enum.auto()
        CATEGORY = enum.auto()

    name: str
    value: object
    target: Target
    data_type: DataType

    def validate(self):
        """Validate to ensure that it will be accepted on upload."""
        if self.target not in StructuredDataItem.Target:
            raise TypeError(
                "StructuredDataItem.target is not a StructuredDataItem.Target"
            )
        if self.data_type not in StructuredDataItem.DataType:
            raise TypeError(
                "StructuredDataItem.data_type is not a StructuredDataItem.DataType"
            )
        if self.data_type == StructuredDataItem.DataType.CONTINUOUS:
            if not isinstance(self.value, (int, float)):
                raise ValueError("StructuredDataItem.value is not continuous")
        elif self.data_type == StructuredDataItem.DataType.CATEGORY:
            pass
        else:
            raise ValueError(f"Unknown StructuredDataItem.data_type `{self.data_type}`")
