#!/usr/bin/env python3
"""Zeff record builder for HousePrice records."""
__version__ = "0.0"

import logging
from typing import Optional
import sqlite3
from zeff.record import *

LOGGER = logging.getLogger("zeffclient.record.builder")


class HousePriceRecordBuilder:
    """Record builder for HousePrice records.

    :param arg: A single string argument set in the zeff.conf file. This
        string may be anything the builder understands (e.g. a URL,
        unique number, full configuration file, etc.).
    """

    def __init__(self, arg: str):
        self.conn = sqlite3.connect(arg)
        self.conn.row_factory = sqlite3.Row

    def __call__(self, model: bool, record_config: str) -> Optional[Record]:
        """Build and return a record.

        :param model: Flag to indicate if the record builder is building
            records for training or for prediction. If model is true then
            it is for prediction, but if false then it is for training and
            any records not to be used for training should be filtered.

        :param record_config: Record configuration string created by
            the record configuration generator.
        """
        LOGGER.info("Begin building ``HousePrice`` record from %s", record_config)
        record = Record(name=record_config)
        target = self.add_structured_data(record, record_config)
        if not model and not target:
            return None
        self.add_unstructured_data(record, record_config)
        LOGGER.info("End building ``HousePrice`` record from %s", record_config)
        return record

    def add_structured_data(self, record, id):
        target_record = False

        # Select all the properties from the database for the record
        sql = f"SELECT * FROM properties WHERE id={id}"
        cursor = self.conn.cursor()
        row = cursor.execute(sql).fetchone()

        # Process each column in the record except for `id` and
        # add it as a structured data item to the structured data
        # object
        for key in row.keys():
            if key == "id":
                continue
            value = row[key]

            # Is the column a continuous or category datatype
            if isinstance(value, (int, float)):
                dtype = DataType.CONTINUOUS
            else:
                dtype = DataType.CATEGORY

            # Is this a target field
            if key in ["estimate_mortgage"] and value is not None:
                target = Target.YES
                target_record = True
            else:
                target = Target.NO

            # Create the structured data item and add it to the
            # structured data object
            sd = StructuredData(name=key, value=value, data_type=dtype, target=target)
            sd.record = record

        # Clean up then add the structured data object to the record
        cursor.close()
        return target_record

    def add_unstructured_data(self, record, id):
        # Select all the property imaages for the record
        sql = f"SELECT * FROM property_images WHERE property_id={id}"
        cursor = self.conn.cursor()

        # Process each row returned in the selection, create an
        # unstructured data item, and add that to the unstructured
        # data object. Note that we are assuming that the file-type
        # for all of these images is a JPEG, but that may be different
        # in your system.
        for row in cursor.execute(sql).fetchall():
            url = row["url"]
            file_type = FileType.IMAGE
            group_by = row["image_type"]
            ud = UnstructuredData(url, file_type, group_by=group_by)
            ud.record = record

        # Clean up then add the unstructured data object to the record
        cursor.close()


if __name__ == "__main__":
    import sys
    from logging import basicConfig, DEBUG
    import errno
    import argparse
    from pathlib import Path
    from zeff.cli import load_configuration
    from zeff.record import format_record_restructuredtext

    if sys.version_info < (3, 7):
        raise Exception("{0} requires Python 3.7.".format(sys.argv[0]))

    basicConfig(level=DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "recordtype",
        choices=["model", "dataset"],
        help="What type of record should be created.",
    )
    parser.add_argument("recordconfig", help="Record configuration string.")
    options = parser.parse_args()
    config = load_configuration()
    try:
        builderarg = config.records.record_builder_arg
        builder = HousePriceRecordBuilder(builderarg)
        record = builder((options.recordtype == "model"), options.recordconfig)
        if options.recordtype == "model" and record == None:
            print("Record is not a training record.")
        else:
            validator = config.records.record_validator((options.recordtype == "model"))
            validator(record)
        format_record_restructuredtext(record, out=sys.stdout)
    except TypeError as err:
        logging.error(f"Record Validation Failed {err}")
        sys.exit(1)
    except ValueError as err:
        logging.error(f"Record Validation Failed {err}")
        sys.exit(1)
    except SystemExit as err:
        logging.info("System exit")
        raise
    except InterruptedError as err:
        logging.info("Interrupt")
    except KeyboardInterrupt as err:
        logging.debug("Keyboard interrupt")
        sys.exit(errno.EINTR)
    except Exception as err:
        logging.exception("Unhandled exception.")
        sys.exit(1)
