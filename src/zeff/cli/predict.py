# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff subcommand to use machine to make a prediction."""
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
__all__ = ["predict_subparser"]

import sys
import logging
from time import sleep

import datetime
import zeff
import zeff.record
from .pipeline import subparser_pipeline, build_pipeline


def predict_subparser(subparsers, config):
    """Add the ``predict`` sub-system as a subparser for argparse.

    :param subparsers: The subparser to add the predict sub-command.
    """

    parser = subparsers.add_parser(
        "predict", help="""Upload record to infer a prediction."""
    )
    parser.add_argument(
        "--model-version",
        type=int,
        help="""Choose a model version to make prediction against. The
            default is the latest valid version.""",
    )
    subparser_pipeline(parser, config)
    parser.set_defaults(func=predict)


def predict(options):
    """Generate a set of records from options."""
    logger = logging.getLogger("zeffclient.record.uploader")
    logger.info("Build prediction pipeline")
    now = datetime.datetime.utcnow()
    try:
        _, records = build_pipeline(
            options, True, zeff.Predictor, options.model_version
        )
    except zeff.cloud.exception.ZeffCloudModelException as err:
        print(err, file=sys.stderr)
        sys.exit(1)
    logger.info("Prediction pipeline starts")
    records = list(records)
    backoff = 1.0
    cutoff = 64.0
    while backoff < cutoff and records:
        sleep(backoff)
        backoff = backoff * 2
        for record in list(records):
            if hasattr(record, "updated_timestamp"):
                # Record is in cloud/Model
                # Need to only look at records that has an updated result
                if record.updated_timestamp > now:
                    records.remove(record)
                    print(record)
            else:
                # Record not added to cloud/Model --- dry-run
                records.remove(record)
                print(record)
    logger.info("Prediction pipeline completes")
    for record in records:
        logger.warning(
            "Predictions not complete %s in dataset %s",
            record.record_id,
            record.dataset_id,
        )
