# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff CLI utility record builders."""
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
__all__ = ["EchoRecordBuilder", "NameRecordBuilder"]

import logging
from zeff.record import Record

LOGGER = logging.getLogger("zeffclient.record.builder")


class EchoRecordBuilder:
    """Prints the config string to stdout and returns no record."""

    # pylint: disable=too-few-public-methods

    def __init__(self, *args, **argv):
        """TBW."""

    def __call__(self, config):
        """TBW."""
        LOGGER.info("Begin building ``Echo`` record from %s", config)
        print(f"Record Config: {config}")
        LOGGER.info("End building ``Echo`` record from %s", config)


class NameRecordBuilder:
    """Creates a record with config string as name."""

    # pylint: disable=too-few-public-methods

    def __init__(self, *args, **argv):
        """TBW."""

    def __call__(self, config):
        """TBW."""
        LOGGER.info("Begin building ``Name`` record from %s", config)
        ret = Record(name=config)
        LOGGER.info("End building ``Name`` record from %s", config)
        return ret
