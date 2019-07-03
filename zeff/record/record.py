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

    def validate(self):
        """Validate to ensure that it will be accepted on upload."""
        # pylint: disable=no-member
        for data in self.structured_data:
            data.validate()
        for data in self.unstructured_data:
            data.validate()
