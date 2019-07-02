"""Zeff record."""
# pylint: disable=too-few-public-methods
__docformat__ = "reStructuredText en"


class Record:
    """This represents a single record in Zeff."""

    def __init__(self, name: str):
        """Create a new record.

        :param name: The name of the record.
        """
        self.name = name
