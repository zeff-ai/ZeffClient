"""Zeff record generation."""
__docformat__ = "reStructuredText en"

import logging
logging = logging.getLogger('zeffclient.record_generator')  # pylint: disable=invalid-name


def generate(record_url_generator, record_builder):
    """Generate a set of records from a record builder.

    :param record_url_generator: A generator that will produce URLs
        from which records may be built. These URLs are are unmodified
        when given to `record_builder`.

    :param record_builder: An callable object that will accept a single
        URL parameter and return a Zeff record type (e.g.
        `zeff.record.Record` or `zeff.temporalrecord.TemporalRecord`).
    """
    logging.info("Begin generating records ...")
    for url in record_url_generator:
        record = record_builder(url)
        yield record
    logging.info("End generating records ...")
