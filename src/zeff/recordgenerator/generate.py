# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff record generation."""
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
__all__ = ["generate"]

import logging

LOGGER = logging.getLogger("zeffclient.record.generator")


def generate(record_url_generator, record_builder):
    """Generate a set of records from a record builder.

    :param record_url_generator: A generator that will produce URLs
        from which records may be built. These URLs are are unmodified
        when given to `record_builder`.

    :param record_builder: An callable object that will accept a single
        URL parameter and return a Zeff record type (e.g.
        `zeff.record.Record` or `zeff.temporalrecord.TemporalRecord`).
    """
    LOGGER.info("Begin generating records ...")
    for url in record_url_generator:
        record = record_builder(url)
        yield record
    LOGGER.info("End generating records ...")
