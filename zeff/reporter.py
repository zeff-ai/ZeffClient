"""Reporter is a protocol that allows tracking of records in the pipeline."""
__copyright__ = """Copyright (C) 2019 Ziff, Inc."""
__docformat__ = "reStructuredText en"

import logging


class Reporter():
    """TBD."""

    def generated(self, record):
        """TBD."""

    def validate_success(self, record):
        """TBD."""

    def validate_warning(self, record, error: Exception):
        """TBD."""

    def validate_error(self, record, error: Exception):
        """TBD."""

    def submit_success(self, record):
        """TBD."""

    def submit_error(self, record, error: Exception):
        """TBD."""


class LoggingReporter(Reporter):
    """TBD.

    Implementation of Reporter protocol that will log reporting events
    to the ``logging.Logger`` object.

    :param logger: The ``logging.Logger`` object to log reporting events.
    """

    def __init__(self, logger: logging.Logger):
        """TBD."""
        self.logger = logger

    def generated(self, record):
        """Log record generated to INFO level."""
        self.logger.info("Record Generated: %s", record)

    def validate_success(self, record):
        """Log record validation success to INFO level."""
        self.logger.info("Record Validated: %s", record)

    def validate_warning(self, record, error: Exception):
        """Log record validation warning to WARNING level."""
        self.logger.warning("Record Validation Warning: %s, %s", record, error)

    def validate_error(self, record, error: Exception):
        """Log record validation error to ERROR level."""
        self.logger.error("Record Validation Error: %s, %s", record, error)

    def submit_success(self, record):
        """Log record submit success to INFO level."""
        self.logger.info("Record Submitted: %s", record)

    def submit_error(self, record, error: Exception):
        """Log record submit error to ERROR level."""
        self.logger.error("Record Validation Error: %s, %s", record, error)
