#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""zeff is a CLI tool that simplifies experimentation with Zeff Cloud API."""
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

import sys

if sys.version_info < (3, 7):
    raise Exception("{0} Requires Python 3.7 or higher.".format(sys.argv[0]))


def main(args=None):
    """Configure system from command line arguments and configuration files."""
    # pylint: disable=broad-except
    # pylint: disable=import-outside-toplevel

    import traceback
    import errno
    import pathlib
    import logging
    import zeff.cli

    zeff.cli.configure_logging()

    cwd = str(pathlib.Path.cwd())
    if cwd not in sys.path:
        sys.path.append(cwd)
    options = zeff.cli.parse_commandline(args=args)

    try:
        logging.info("Starting with options %s", options)
        options.func(options)
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


if __name__ == "__main__":
    main()
