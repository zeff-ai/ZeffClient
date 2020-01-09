# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff subcommand to upload records."""
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
__all__ = ["upload_subparser"]

import logging
import zeff
import zeff.record
from .pipeline import subparser_pipeline, build_pipeline
from .train import Trainer


def upload_subparser(subparsers, config):
    """Add the ``upload`` sub-system as a subparser for argparse.

    :param subparsers: The subparser to add the upload sub-command.
    """

    parser = subparsers.add_parser(
        "upload", help="""Build, validate, and upload training records."""
    )
    subparser_pipeline(parser, config)
    parser.add_argument(
        "--no-train",
        action="store_true",
        help="""Build, validate, and upload training records, but do not
            start training of machine.""",
    )
    parser.set_defaults(func=upload)


def upload(options):
    """Generate a set of records from options."""
    logger = logging.getLogger("zeffclient.record.uploader")
    logger.info("Build upload pipeline")
    counter, records = build_pipeline(options, False, zeff.Uploader)
    logger.info("Upload pipeline starts")
    for record in records:
        logger.info("Record Count %d", counter.count)
        logger.debug(record)
    logger.info("Upload pipeline completes")
    logging.info("Records uploaded %d", counter.count)
    if counter.count == 0 and not options.no_train:
        logger.info("Start training the model")
        logger.debug("All records uploaded, start training.")
        trainer = Trainer(options)
        trainer.start()
    logger.info("Upload process completes")
