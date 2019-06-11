#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ----------------------------------------------------------------------------
"""zeff is a CLI tool that simplifies experimentation with Zeff Cloud API."""
__copyright__ = """Copyright (C) 2019 Ziff, Inc."""
__docformat__ = "reStructuredText en"

import sys
if sys.version_info < (3, 7):
    raise Exception("{0} Requires Python 3.7 or higher.".format(sys.argv[0]))
import os
import traceback
import errno
import logging
import datetime
import zeff

def parse_commandline(process_name, *args):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {zeff.__version__}")
    parser.add_argument(
        '--verbose',
        type=str,
        default='warning',
        choices=['critical', 'error', 'warning', 'info', 'debug'],
        help='Change default logging verbosity.')
    parser.add_argument(
        '--logging-conf',
        type=str,
        default=os.path.join(os.path.dirname(__file__), "logging_default.txt"),
        help='Logging configuration file.')
    options = parser.parse_args(args=args)

    if options.verbose == 'debug':
        print("Working directory:", os.getcwd(), file=sys.stderr)

    return options


def main():
    """Configure system from command line arguments and configuration files."""

    process_name = os.path.basename(sys.argv[0])
    root_dir = os.path.dirname(sys.argv[0])
    if os.path.basename(root_dir) in ['bin', 'lib', 'libexec']:
        root_dir = os.path.dirname(root_dir)
    args = sys.argv[1:]
    options = parse_commandline(process_name, *args)

    try:
        import ast
        import logging.config
        with open(options.logging_conf, 'r') as f:
            d = ast.literal_eval(f.read())
            logging.config.dictConfig(d)
    except Exception as err:
        if options.verbose == "debug":
            traceback.print_exception(err.__class__, err, err.__traceback__, file=sys.stderr)
        else:
            print("Unhandled exception while configuring logging:", err, file=sys.stderr)
        sys.exit(1)

    try:
        logging.info("Starting with options %s", options)
        print("NO PROCESSING OCCURS YET")
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
